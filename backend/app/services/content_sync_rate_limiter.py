from collections import deque
from time import monotonic

from app.core.config import settings


class ContentSyncRateLimiter:
    def __init__(self) -> None:
        self._requests_by_token: dict[str, deque[float]] = {}

    def allow(self, token: str, now: float | None = None) -> bool:
        current_time = monotonic() if now is None else now
        request_times = self._requests_by_token.setdefault(token, deque())
        window_start = current_time - settings.content_sync_rate_limit_window_seconds

        while request_times and request_times[0] <= window_start:
            request_times.popleft()

        if len(request_times) >= settings.content_sync_rate_limit_max_requests:
            return False

        request_times.append(current_time)
        return True

    def reset(self) -> None:
        self._requests_by_token.clear()


content_sync_rate_limiter = ContentSyncRateLimiter()
