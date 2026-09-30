from __future__ import annotations

import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, limit: int = 10, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self._store: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.time()
        bucket = self._store[key]
        while bucket and bucket[0] <= now - self.window_seconds:
            bucket.popleft()
        if len(bucket) >= self.limit:
            return False
        bucket.append(now)
        return True

    def remaining(self, key: str) -> int:
        now = time.time()
        bucket = self._store[key]
        while bucket and bucket[0] <= now - self.window_seconds:
            bucket.popleft()
        return max(self.limit - len(bucket), 0)


def build_rate_limiter(enabled: bool = True, limit: int = 10, window_seconds: int = 60) -> RateLimiter | None:
    if not enabled:
        return None
    return RateLimiter(limit=limit, window_seconds=window_seconds)


def check_rate_limit(limiter: RateLimiter | None, key: str) -> bool:
    if limiter is None:
        return True
    return limiter.allow(key)
