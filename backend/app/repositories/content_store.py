import json
import sqlite3
from pathlib import Path

from app.core.config import settings
from app.schemas.content_sync import ContentBundleImportRequest, ContentBundleImportResult
from app.schemas.question import QuestionDetail

_SCHEMA = """
CREATE TABLE IF NOT EXISTS content_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bundle_version TEXT NOT NULL UNIQUE,
    source_commit TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS source_documents (
    snapshot_id INTEGER NOT NULL,
    document_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    part TEXT NOT NULL,
    title TEXT,
    source_path TEXT NOT NULL,
    PRIMARY KEY (snapshot_id, document_id),
    FOREIGN KEY (snapshot_id) REFERENCES content_snapshots(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS question_records (
    snapshot_id INTEGER NOT NULL,
    question_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    part TEXT NOT NULL,
    title TEXT,
    type TEXT NOT NULL,
    prompts_json TEXT NOT NULL,
    answers_json TEXT NOT NULL,
    aliases_json TEXT NOT NULL,
    keywords_json TEXT NOT NULL,
    warnings_json TEXT NOT NULL,
    source_path TEXT NOT NULL,
    source_line INTEGER NOT NULL,
    PRIMARY KEY (snapshot_id, question_id),
    FOREIGN KEY (snapshot_id) REFERENCES content_snapshots(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_question_records_active
ON question_records (snapshot_id, unit_id, part);
"""


class ContentStore:
    def initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(_SCHEMA)

    def import_bundle(self, payload: ContentBundleImportRequest) -> ContentBundleImportResult:
        self.initialize()

        with self._connect() as connection:
            existing = connection.execute(
                """
                SELECT id
                FROM content_snapshots
                WHERE bundle_version = ?
                """,
                (payload.manifest.bundleVersion,),
            ).fetchone()
            if existing is not None:
                snapshot_id = int(existing["id"])
                self._activate_snapshot(connection, snapshot_id)
                return ContentBundleImportResult(
                    snapshotId=snapshot_id,
                    importedBundleVersion=payload.manifest.bundleVersion,
                    importedQuestionCount=self._count_rows(connection, "question_records", snapshot_id),
                    importedDocumentCount=self._count_rows(connection, "source_documents", snapshot_id),
                    reusedSnapshot=True,
                )

            cursor = connection.execute(
                """
                INSERT INTO content_snapshots (
                    bundle_version,
                    source_commit,
                    generated_at,
                    content_hash,
                    is_active
                ) VALUES (?, ?, ?, ?, 0)
                """,
                (
                    payload.manifest.bundleVersion,
                    payload.manifest.sourceCommit,
                    payload.manifest.generatedAt,
                    payload.manifest.contentHash,
                ),
            )
            snapshot_id = int(cursor.lastrowid)

            connection.executemany(
                """
                INSERT INTO source_documents (
                    snapshot_id,
                    document_id,
                    unit_id,
                    part,
                    title,
                    source_path
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        snapshot_id,
                        document.documentId,
                        document.unitId,
                        document.part,
                        document.title,
                        document.sourcePath,
                    )
                    for document in payload.documents
                ],
            )

            connection.executemany(
                """
                INSERT INTO question_records (
                    snapshot_id,
                    question_id,
                    unit_id,
                    part,
                    title,
                    type,
                    prompts_json,
                    answers_json,
                    aliases_json,
                    keywords_json,
                    warnings_json,
                    source_path,
                    source_line
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        snapshot_id,
                        question.questionId,
                        question.unitId,
                        question.part,
                        question.title,
                        question.type,
                        self._encode_list(question.prompts),
                        self._encode_list(question.answers),
                        self._encode_list(question.aliases),
                        self._encode_list(question.keywords),
                        self._encode_list(question.warnings),
                        question.sourcePath,
                        question.sourceLine,
                    )
                    for question in payload.questions
                ],
            )

            self._activate_snapshot(connection, snapshot_id)
            return ContentBundleImportResult(
                snapshotId=snapshot_id,
                importedBundleVersion=payload.manifest.bundleVersion,
                importedQuestionCount=len(payload.questions),
                importedDocumentCount=len(payload.documents),
            )

    def list_active_questions(self) -> list[QuestionDetail]:
        if not Path(settings.sqlite_path).exists():
            return []

        self.initialize()

        with self._connect() as connection:
            snapshot_id = self._get_active_snapshot_id(connection)
            if snapshot_id is None:
                return []

            rows = connection.execute(
                """
                SELECT
                    question_id,
                    unit_id,
                    part,
                    title,
                    type,
                    prompts_json,
                    answers_json,
                    aliases_json,
                    keywords_json,
                    warnings_json,
                    source_path,
                    source_line
                FROM question_records
                WHERE snapshot_id = ?
                ORDER BY question_id
                """,
                (snapshot_id,),
            ).fetchall()
            return [self._row_to_question(row) for row in rows]

    def has_active_snapshot(self) -> bool:
        if not Path(settings.sqlite_path).exists():
            return False

        self.initialize()
        with self._connect() as connection:
            return self._get_active_snapshot_id(connection) is not None

    def _connect(self) -> sqlite3.Connection:
        sqlite_path = Path(settings.sqlite_path)
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(sqlite_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _activate_snapshot(self, connection: sqlite3.Connection, snapshot_id: int) -> None:
        connection.execute("UPDATE content_snapshots SET is_active = 0")
        connection.execute(
            "UPDATE content_snapshots SET is_active = 1 WHERE id = ?",
            (snapshot_id,),
        )

    def _get_active_snapshot_id(self, connection: sqlite3.Connection) -> int | None:
        row = connection.execute(
            """
            SELECT id
            FROM content_snapshots
            WHERE is_active = 1
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()
        if row is None:
            return None
        return int(row["id"])

    def _count_rows(self, connection: sqlite3.Connection, table_name: str, snapshot_id: int) -> int:
        row = connection.execute(
            f"SELECT COUNT(*) AS count FROM {table_name} WHERE snapshot_id = ?",
            (snapshot_id,),
        ).fetchone()
        return int(row["count"])

    def _row_to_question(self, row: sqlite3.Row) -> QuestionDetail:
        return QuestionDetail(
            questionId=row["question_id"],
            unitId=row["unit_id"],
            part=row["part"],
            title=row["title"],
            type=row["type"],
            prompts=self._decode_list(row["prompts_json"]),
            answers=self._decode_list(row["answers_json"]),
            aliases=self._decode_list(row["aliases_json"]),
            keywords=self._decode_list(row["keywords_json"]),
            warnings=self._decode_list(row["warnings_json"]),
            sourcePath=row["source_path"],
            sourceLine=int(row["source_line"]),
        )

    def _encode_list(self, values: list[str]) -> str:
        return json.dumps(values, ensure_ascii=True)

    def _decode_list(self, payload: str) -> list[str]:
        return json.loads(payload)
