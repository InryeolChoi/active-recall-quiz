# Frontend Source Transition Review

## Scope

This review covers how the frontend reacts when the data source moves from local `unit_*` markdown files to an external `active-recall-notes` repository plus SQLite-backed storage.

The goal is to separate changes that must happen immediately from changes that can wait until the backend contract is finalized.

## Current Frontend Contract

The UI currently depends on a stable unit/question contract:

- Home and exam pages load units for summaries and selection.
- Study mode filters questions by `unitId` and `part`.
- Exam setup sends `unitIds`, `parts`, `questionCount`, `mode`, and `shuffle`.
- Exam detail and result screens assume exam and grading payloads remain shaped around stable question ids.

The most visible contract fields are:

- `UnitSummary`: `unitId`, `title`, `parts`, `questionCount`
- `QuestionDetail`: `questionId`, `unitId`, `part`, `title`, `prompts`, `answers`, `aliases`, `keywords`, `warnings`
- `ExamDetail`: `examId`, `mode`, `createdAt`, `unitIds`, `parts`, `questionCount`, `questions`
- `GradingResult`: `examId`, `score`, `total`, `submittedAt`, `results`

## Immediate Impact

These items need attention as soon as the backend contract changes:

- If `unitId` is renamed or removed, unit pickers and study filters will break.
- If `parts` changes shape, both study filtering and exam setup will need updates.
- If question titles/prompts/aliases/keywords are dropped, study cards and exam labels will need new fallback text.
- If `createExam` stops accepting `unitIds` and `parts`, the exam setup form must be rewritten.
- If `getUnits` becomes paginated or source-specific, the home and exam pages must stop assuming a complete in-memory list.

## Safe To Defer

These changes can wait until the backend schema and sync pipeline are stable:

- Adding extra source metadata from SQLite.
- Showing repository provenance, source file paths, or source line numbers in the UI.
- Changing copy that mentions "markdown" as long as the visible workflow still works.
- Adapting to new storage internals if the API shape stays compatible.

## Contract Dependencies

### Backend Analysis `#30`

The frontend should not need to know how `unit_*` paths are removed, as long as the backend keeps returning the same logical unit/question identifiers. The important boundary is the response shape, not the storage mechanism.

### SQLite Schema `#31`

Schema changes are safe for the frontend only if record identifiers and question grouping stay stable. If the schema introduces new ids or new grouping rules, the frontend selection flow needs to be updated together with the API contract.

### Sync Flow `#32`

The sync pipeline should produce stable ids, stable unit titles, and stable part grouping. If sync introduces partial updates or delayed availability, the UI may need loading and empty-state copy adjustments.

## Recommended Order

1. Keep the current `UnitSummary` and `QuestionDetail` shape stable until the backend migration is ready.
2. Let the backend absorb source normalization and SQLite mapping first.
3. Update the frontend only when a contract change is unavoidable.
4. Remove `markdown` wording from the UI copy only after the new source flow is confirmed.

## Checklist

- [x] Identify the frontend pages that depend on unit/question contracts
- [x] Separate immediate breakpoints from deferred changes
- [x] Connect the review to `#30`, `#31`, and `#32`
- [x] Keep the work limited to documentation
