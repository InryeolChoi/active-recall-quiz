# SQLite Operations Strategy

This document fixes the operational contract for how `active-recall-quiz` should run SQLite after the notes sync migration.
It bridges the schema work in `#31`, the sync design in `#32`, and the importer path in `#41` so that `active-recall-notes` CI/CD can target a clear runtime destination.

## Decision Summary

- SQLite is the local source of truth for quiz runtime data.
- The notes repository remains the content source of truth.
- Syncing is a write operation, but normal user-facing API traffic should remain read-only.
- The same schema should be used in local, dev, and prod; only the storage path, persistence volume, and trigger mechanism should differ.

## File Location

### Recommended Default

- Keep the repository-local default at `backend/data/content.db` for local development and test environments.
- Treat this as the fallback path, not the long-term production target.

### Production Target

- Use a persistent mounted path outside the application source tree.
- Recommended production mount path: `/var/lib/active-recall-quiz/content.db`.
- The app container should see the database through a volume mount, not a committed file.

### Environment Separation

- Local: disposable DB file in the repository workspace.
- Dev: persistent but resettable DB volume for integration testing.
- Prod: persistent DB volume with backup and restore policy.

## Initialization

- The database file should be created on first sync or first startup if it does not exist.
- Schema creation must be deterministic and repeatable.
- The importer should bootstrap an empty database before attempting to write content snapshots.
- Schema migrations should be explicit, not implicit side effects of API traffic.

## Runtime Placement

- The actual import logic should run inside the `active-recall-quiz` backend runtime or a dedicated backend job using the same codebase.
- It should not run in the frontend and should not run inside `active-recall-notes`.
- User requests should read from SQLite only.
- Content sync is the only flow that writes to the database.

## Write Permissions

- Normal API request handlers should not require write access except where they need to record runtime state that is already part of the backend design.
- The sync job or sync endpoint needs write access to the SQLite file and the backup location.
- `active-recall-notes` CI/CD should never write the database directly; it should only trigger or deliver content to the quiz backend.
- If file permissions are tightened in production, the sync process should be the only actor with mutation rights on the DB volume.

## Backup And Restore

- Take a backup before applying a new snapshot.
- Keep the last known good database available until the new import validates successfully.
- Prefer atomic replace semantics: write to a staging file, validate, then swap into the live path.
- Preserve enough history to restore the previous good snapshot if the new import or validation fails.

## Suggested Operational Flow

1. `active-recall-notes` produces a versioned export artifact.
2. `active-recall-quiz` receives the artifact through CI/CD, dispatch, or a scheduled pull.
3. The backend importer writes to a staging database.
4. Validation runs against the staging database.
5. The staging database becomes the live SQLite file only after validation succeeds.
6. The previous live database is retained as a rollback point until the new state is confirmed.

## CI/CD Target Contract

The external notes repository should target a single quiz-backend ingestion surface:

- authenticated trigger or artifact handoff only
- no direct filesystem access to the SQLite volume
- idempotent import of the same bundle version
- explicit source commit or bundle version in every sync request

This means `active-recall-notes` can safely automate content release without knowing the internal SQLite layout.

## Failure Policy

- If artifact validation fails, the live database must remain unchanged.
- If the import fails midway, the partially written state must not become active.
- If a newer bundle is invalid, the previous good snapshot stays in service.
- Sync failures should be observable through logs that include source commit, bundle version, and failure reason.

## Open Assumptions

- The current repository-local default path is acceptable for local work, but production should move to a mounted volume.
- The importer should be able to create the database file on demand.
- `active-recall-notes` will emit a versioned artifact or dispatch event before this repository applies the import.

