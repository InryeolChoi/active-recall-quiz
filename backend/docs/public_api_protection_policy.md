# Public API Protection Policy

This document defines the minimum protection policy for the public read APIs in `active-recall-quiz`.
It records what must be protected immediately and what can be hardened later as traffic grows.

## Scope

Public endpoints in scope:

- `GET /api/units`
- `GET /api/questions`
- `GET /api/questions/{questionId}`
- `GET /api/exams`
- `GET /api/exams/{examId}`
- `GET /api/exams/{examId}/result`
- `POST /api/exams/{examId}/submit`
- `POST /api/content-sync/bundles`

The sync endpoint is the most sensitive route because it mutates SQLite.
Read endpoints remain public for the frontend, but they still need basic abuse controls.

## Current Posture

- Runtime content is already served from SQLite after notes sync imports an active snapshot.
- `POST /api/content-sync/bundles` is protected by `X-Content-Sync-Token`.
- The backend currently allows broad CORS origins, so CORS should not be treated as an auth layer.
- The frontend is deployed separately and reads from the backend API.

## Immediate Protection

### 1. Protect sync first

- Keep `POST /api/content-sync/bundles` token-protected at all times.
- Apply the first rate limit here, not on the read endpoints.
- Tune the limit so normal `active-recall-notes` reruns stay safe and idempotent.

Recommended immediate behavior:

- allow small bursts for legitimate CI/CD retries
- reject excessive repeated sync attempts
- keep repeated bundle re-imports idempotent

### 2. Keep read APIs available

- Do not block the public read APIs behind auth.
- Keep them stable for the frontend and for direct debugging.
- Watch usage on `/api/units` and `/api/questions`, since these are the most likely hot paths.

### 3. Narrow CORS later

- Open CORS should be treated as a development convenience, not a security boundary.
- Narrow CORS to the deployed frontend origin once the production frontend URL is stable.
- Keep localhost origins only for local development.

### 4. Log the right events

Minimum logs to keep:

- sync request start
- sync request success
- sync request failure
- auth failure
- validation failure
- repeated bundle reuse

For sync requests, include:

- bundle version
- source commit
- request result
- failure reason when applicable

## Later Hardening

These items should follow once the current release is stable.

- Per-route rate limiting for `GET /api/units` and `GET /api/questions`
- IP-based throttling for repeated public access
- CDN or WAF protection in front of the backend
- Response caching for stable read endpoints
- Structured metrics for sync volume and failure rate
- Alerting for repeated sync failures or traffic spikes

## Operational Guidance

### Immediate response

When traffic or abuse increases:

- keep sync token protection enabled
- inspect backend logs for bundle version and source commit
- confirm whether the caller is a legitimate notes rerun
- reduce retry windows if repeated noise appears

### Escalation path

If abuse continues:

- narrow CORS to the deployed frontend origin only
- add a small limiter to the public read APIs
- place a proxy or CDN with throttling in front of the backend
- rotate the sync token if exposure is suspected

## Completion Criteria

This policy is satisfied for the current release when:

- `content-sync` remains token-protected
- the public read APIs continue serving the frontend
- logs are sufficient to trace sync requests
- no write access is exposed through public read routes

The items in the later hardening section should be tracked separately when traffic or operational risk justifies them.
