# Content Sync Runtime Validation

This note records the runtime validation performed for `#44` against the content sync endpoint added in `#41`, using the SQLite operating contract defined in `#45`.

## Validation Environment

- Worktree branch: `feature/44-content-sync-runtime-validation`
- Python runtime: `uv`-managed CPython `3.13.11`
- Dependency install: `uv pip install --python .venv/bin/python -r backend/requirements.txt`
- App server: `../.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001`
- SQLite target path during validation: `backend/data/content.db`

## Runtime Checks

### 1. Server health

- Request: `GET /health`
- Result: `200 OK`
- Response body: `{"status":"ok"}`

### 2. Successful bundle import

- Request: `POST /api/content-sync/bundles`
- Bundle version used: `bundle-20260324-runtime-001`
- Result: `200 OK`
- Response body summary:
  - `snapshotId = 1`
  - `importedQuestionCount = 1`
  - `importedDocumentCount = 1`
  - `reusedSnapshot = false`

### 3. SQLite file creation

- Generated file confirmed at `backend/data/content.db`
- SQLite query result after import:
  - active snapshots: `1`
  - documents stored: `1`
  - questions stored: `1`

Observed snapshot row:

```json
{
  "id": 1,
  "bundle_version": "bundle-20260324-runtime-001",
  "source_commit": "abc123def456",
  "is_active": 1
}
```

### 4. Runtime read path after import

- Request: `GET /api/units`
- Result: imported unit summary returned from the active snapshot

- Request: `GET /api/questions`
- Result: imported question record returned from the active snapshot

This confirms the runtime read path prefers SQLite-backed content once an active snapshot exists.

### 5. Idempotent re-import

- Same bundle posted a second time
- Result: `200 OK`
- Response body summary:
  - `snapshotId = 1`
  - `reusedSnapshot = true`

This matches the intended bundle reuse behavior from `#41`.

### 6. Invalid request handling

- Request body omitted `manifest`
- Result: `422 Unprocessable Content`
- Response body:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "manifest"],
      "msg": "Field required",
      "input": {
        "documents": [],
        "questions": []
      }
    }
  ]
}
```

## Observed Logs

The server emitted the expected request-level logs for:

- `GET /health -> 200`
- `POST /api/content-sync/bundles -> 200`
- repeated `POST /api/content-sync/bundles -> 200`
- invalid `POST /api/content-sync/bundles -> 422`
- `GET /api/units -> 200`
- `GET /api/questions -> 200`

These are sufficient for local validation, but production sync should add structured logging around bundle version, source commit, and failure reason.

## CI/CD Readiness Assessment

What is ready now:

- The backend can receive a content bundle over HTTP.
- A successful request creates the SQLite file if it does not already exist.
- Imported content becomes the active runtime source.
- Reposting the same bundle version is idempotent.
- Invalid payloads fail fast with schema validation.

What still needs attention before production CI/CD:

- The endpoint is currently unauthenticated.
- There is no staging DB swap or backup/restore flow yet.
- Validation is local-only; deploy-target path and secret handling still need environment-specific wiring.

## Conclusion

`#41` is runtime-viable for a first end-to-end sync in local validation:

- app starts successfully
- content sync writes SQLite
- runtime reads the imported snapshot
- malformed requests return `422`

This is enough to continue toward external CI/CD integration, but production rollout should add authentication and rollout safeguards before `active-recall-notes` pushes data automatically.
