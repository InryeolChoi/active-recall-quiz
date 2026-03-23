from pydantic import BaseModel, Field

from app.schemas.question import QuestionDetail


class ContentManifest(BaseModel):
    bundleVersion: str
    sourceCommit: str
    generatedAt: str
    contentHash: str


class SourceDocumentRecord(BaseModel):
    documentId: str
    unitId: str
    part: str
    title: str | None = None
    sourcePath: str


class ImportedQuestionRecord(QuestionDetail):
    pass


class ContentBundleImportRequest(BaseModel):
    manifest: ContentManifest
    documents: list[SourceDocumentRecord] = Field(default_factory=list)
    questions: list[ImportedQuestionRecord] = Field(default_factory=list)


class ContentBundleImportResult(BaseModel):
    snapshotId: int
    importedBundleVersion: str
    importedQuestionCount: int
    importedDocumentCount: int
    reusedSnapshot: bool = False
