# Issue #30 Unit Dependency Analysis

## Scope

This analysis covers the current backend paths that still assume `unit_*` local markdown folders as the data source.
It focuses on parser, loader, service, API, and test coupling, and it highlights the boundary that should later move to the external notes repository flow.

## Where `unit_*` Is Baked In

- [`backend/app/core/config.py`](/Users/inchoi/active_recall_quiz/backend/app/core/config.py) sets the default `content_glob` to `unit_*/*.md`, so the backend discovers content by scanning local unit folders.
- [`backend/app/parsers/loader.py`](/Users/inchoi/active_recall_quiz/backend/app/parsers/loader.py) uses that glob directly, so every content load begins from the local filesystem layout.
- [`backend/app/parsers/markdown_parser.py`](/Users/inchoi/active_recall_quiz/backend/app/parsers/markdown_parser.py) derives `unit_id` from `path.parent.name` and `part` from `path.stem`, which means the folder name is part of the domain model.
- [`backend/app/parsers/normalizer.py`](/Users/inchoi/active_recall_quiz/backend/app/parsers/normalizer.py) builds `questionId` values from `unit_id`, so downstream identifiers depend on the folder-based source model.
- [`backend/app/services/question_service.py`](/Users/inchoi/active_recall_quiz/backend/app/services/question_service.py) groups questions by `unitId`, exposes unit summaries, and loads all questions from the parser pipeline.
- [`backend/app/api/routes_units.py`](/Users/inchoi/active_recall_quiz/backend/app/api/routes_units.py) exposes `/units`, which is effectively a view over the local unit grouping.
- [`backend/app/api/routes_questions.py`](/Users/inchoi/active_recall_quiz/backend/app/api/routes_questions.py) keeps `unitId` as a public filter, so the API contract still reflects unit-scoped navigation.
- [`backend/app/services/exam_service.py`](/Users/inchoi/active_recall_quiz/backend/app/services/exam_service.py) carries `unitIds` into exam creation and snapshots questions in a unit-aware shape.
- [`backend/app/services/stats_service.py`](/Users/inchoi/active_recall_quiz/backend/app/services/stats_service.py) infers the unit from `questionId`, so weakness stats still depend on the same unit naming scheme.

## Tests That Lock the Current Shape

- [`backend/tests/test_parser.py`](/Users/inchoi/active_recall_quiz/backend/tests/test_parser.py) reads `unit_1_1/part1.md` directly and asserts the parsed `unit_id`.
- [`backend/tests/test_grading.py`](/Users/inchoi/active_recall_quiz/backend/tests/test_grading.py) uses a hard-coded `unit_1_1:part1:1` question id.
- [`backend/tests/test_api_contract.py`](/Users/inchoi/active_recall_quiz/backend/tests/test_api_contract.py) verifies `unitId` filtering, unit summaries, and weakness stats structure.

## Impact Summary

- Parser impact: high. The parsing model currently assumes that file system structure defines the domain identity.
- Loader impact: high. Content discovery cannot be swapped without changing the glob source.
- Service impact: high. Question, exam, and stats services all consume `unitId` as a stable concept.
- API impact: medium to high. `/questions`, `/units`, and weakness stats expose unit-shaped responses that would need a new source mapping.
- Test impact: high. Existing tests encode the current `unit_*` path and identifier format.

## What Can Be Removed Later

- Local file discovery through `content_glob` once the backend reads from SQLite or another normalized store.
- Direct parsing of markdown files inside the runtime question-loading path.
- Folder-name-derived `unit_id` extraction once the external repository provides stable metadata or the database stores canonical ids.

## What Needs Replacement

- `iter_markdown_files()` should be replaced by a repository/database loader.
- `parse_markdown_file()` and `normalize_parsed_file()` should become import/sync-time utilities, not runtime dependencies.
- Unit summary generation should be backed by stored metadata rather than reconstructed from file layout.
- `questionId` generation should move to the ingestion layer if ids must remain stable after folder removal.

## Suggested Migration Order

1. Introduce a persisted content model or sync snapshot that stores unit, part, and question metadata independent of folder structure.
2. Repoint `QuestionService` to load from the persisted model while keeping the API response shape stable.
3. Replace runtime markdown globbing with ingestion-time parsing from `active-recall-notes`.
4. Update `/units` and weakness stats to read canonical stored metadata rather than parsing ids.
5. Rewrite tests to fixture-driven database or repository snapshots instead of local `unit_*` files.

## Risks

- Removing `unit_*` too early will break question ids, unit summaries, and test fixtures at the same time.
- Weakness stats currently infer unit identity from the `questionId` string, so id changes will silently alter analytics.
- The current API contract is coupled to unit navigation, so frontend callers may need a coordinated transition.
- If ingestion and runtime parsing are separated without a canonical id strategy, duplicate or drifting question ids can appear.

## Test Gaps To Add

- A fixture-backed loader test that does not depend on `unit_*` file paths.
- A service test proving that unit summaries still work after the source moves off the filesystem.
- A stats test that validates weakness aggregation from persisted metadata rather than id splitting.
- An API contract test for the future non-filesystem content source.

## Frontend Boundary

- The frontend still consumes `/units`, `unitId` filters, and weakness stats, so any backend source swap must preserve those shapes or ship a coordinated API update.
- The backend change can be isolated from frontend UI work only if the response schema remains stable during the first migration step.
