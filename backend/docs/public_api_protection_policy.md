# Public API Protection Policy

This document records the minimum protection policy for public read endpoints in `active-recall-quiz`.
It covers the current runtime posture after the notes-sync migration and separates immediate safeguards from later hardening work.

## Scope

Protected surfaces:

- `GET /api/units`
- `GET /api/questions`
- `GET /api/questions/{questionId}`
- `GET /api/exams`
- `GET /api/exams/{examId}`
- `GET /api/exams/{examId}/result`
- `POST /api/exams/{examId}/submit`
- `POST /api/content-sync/bundles`

The sync endpoint is write-sensitive and should be treated as the highest-risk route.
Read endpoints are public by design, but they still need basic abuse controls once traffic grows.

## Current Posture

- Runtime content is served from SQLite after notes sync imports an active snapshot.
- Notes ingestion already requires `X-Content-Sync-Token`.
- The backend currently allows broad CORS origins and should not rely on CORS as an access control boundary.
- The frontend is deployed separately and only consumes the backend API.

## Immediate Policy

### 1. Rate limit target

- Apply the first rate limit to `POST /api/content-sync/bundles`.
- Keep the limit loose enough to allow normal notes CI/CD retries and idempotent re-syncs.
- Treat repeated auth failures or burst traffic as a signal to tighten the policy later.

Recommended immediate rule:

- low request volume per token and per source IP
- short burst allowance for reruns
- retry-safe so the same bundle can be posted again without operational breakage

### 2. Public read endpoints

- Keep the read API publicly reachable for the frontend.
- Prefer server-side read efficiency instead of blocking access outright.
- Watch for heavy callers on `/api/units` and `/api/questions`, because these are the primary list endpoints hit by the UI.

### 3. CORS

- Do not use open CORS as a security feature.
- Narrow CORS to the deployed frontend origin when the production frontend URL is stable.
- Keep localhost and development origins only for local development.

### 4. Logging

Log the following events at minimum:

- sync request start
- sync request success
- sync request failure
- auth failure
- validation failure
- repeated bundle reuse

For each sync request, include:

- bundle version
- source commit
- request outcome
- failure reason when applicable

## Later Hardening

These items are important, but they can follow the first production-ready sync rollout.

- Per-route rate limiting for `GET /api/units` and `GET /api/questions`
- IP-based throttling for repeated public API access
- CDN or WAF protection in front of the backend
- Response caching for stable read endpoints
- Structured metrics for sync volume and failure rate
- Alerting for repeated sync failures or abnormal request spikes

## Operational Guidance

### Immediate response

Use the following as the first response plan when traffic or abuse increases:

- keep `content-sync` token protection enabled
- reduce the sync retry window if repeated noise appears
- inspect backend logs for bundle version and source commit
- confirm whether the call pattern is a legitimate notes re-run

### Escalation path

If abuse continues:

- narrow CORS to the deployed frontend origin only
- add a small rate limiter on the public GET endpoints
- place a proxy or CDN with throttling in front of the backend
- rotate the sync token if the secret is suspected to be exposed

## Completion Criteria

This policy is considered satisfied for the current release when:

- `content-sync` remains token-protected
- the backend can serve public read traffic without exposing write access
- logs show enough information to trace sync requests
- the frontend can keep reading from the backend without extra changes

The remaining items in the "Later Hardening" section should be tracked separately once traffic or operational needs justify them.
