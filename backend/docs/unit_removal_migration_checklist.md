# Issue #40 Unit Removal Migration Checklist

## Purpose

This checklist defines when it is safe to delete the local `unit_*` folders.
Deletion is the final step of the migration and must happen only after the new notes ingestion flow is live, validated, and observed in production-like conditions.

## Gate Before Deletion

- `#29` frontend impact review is complete.
- `#30` backend `unit_*` dependency analysis is complete.
- `#31` SQLite schema design is complete and implemented.
- `#32` sync flow design is complete.
- `#40` checklist is approved.
- `#41` ingestion pipeline is implemented and importing real content into SQLite.
- `active-recall-notes` CI/CD is producing the expected export artifact.
- No runtime code path scans local markdown files as the source of truth.

## Checklist

### 1. Data Pipeline Readiness

- [ ] `active-recall-notes` export artifact is generated from a known source commit.
- [ ] The export bundle has a manifest with version, hash, and source commit metadata.
- [ ] The importer in this repository can read the bundle without manual intervention.
- [ ] Import is idempotent for the same bundle version.
- [ ] Validation fails before any live table mutation if the bundle is malformed.
- [ ] A successful import records the last applied bundle version.

### 2. SQLite Validation

- [ ] SQLite contains the full expected content set after import.
- [ ] Canonical ids for units, parts, and questions are stable after folder removal.
- [ ] Duplicate content ids are rejected or merged by a documented rule.
- [ ] Existing exam, result, and stats records still resolve against the new ids.
- [ ] Rollback to the previous good snapshot works after a failed import.

### 3. API Behavior

- [ ] `/units` or its replacement is backed by SQLite data, not filesystem discovery.
- [ ] `/questions`, `/exams`, and weakness stats still behave as expected.
- [ ] API contract tests pass against the SQLite-backed source.
- [ ] Any response shape change is documented before the delete step begins.
- [ ] No response field depends on folder names unless the field is intentionally preserved.

### 4. Frontend Impact

- [ ] Frontend signoff is complete for the current API contract.
- [ ] If the API contract changes, frontend updates are included in the same release.
- [ ] Exam creation, study mode, and result views work against SQLite-backed data.
- [ ] No screen still depends on local file paths or folder-shaped assumptions.

### 5. Test Hardening

- [ ] Parser and loader tests no longer require local `unit_*` file paths.
- [ ] Importer tests cover repeated runs, malformed bundles, and rollback behavior.
- [ ] API contract tests cover the SQLite-backed source of truth.
- [ ] E2E or integration coverage exists for the notes import and quiz read path.
- [ ] Test fixtures are updated to use snapshot data instead of raw markdown files.

### 6. Delete Gate

- [ ] Deletion is done in a separate PR after the new source path is green.
- [ ] `unit_*` folders are removed only after all runtime reads are migrated.
- [ ] A rollback plan exists for restoring the last good snapshot and the old folders if needed.
- [ ] Release notes clearly state that SQLite is now the source of truth.
- [ ] A follow-up check confirms there are no remaining references to `unit_*` in runtime paths.

## Rollback Criteria

Do not delete `unit_*` yet if any of the following is true:

- Import fails or produces partial data.
- SQLite validation does not match the source snapshot.
- API contract tests fail after migration.
- Frontend behavior depends on a response shape that is not yet stable.
- Runtime code still reads from the filesystem.
- The last known good SQLite snapshot cannot be restored quickly.

## Recommended Order

1. Finish `#41` and confirm real content is flowing into SQLite.
2. Run the validation checklist and make the importer idempotent.
3. Verify API and frontend behavior against the new source.
4. Harden tests and update fixtures.
5. Remove `unit_*` folders in a final, separate PR.

