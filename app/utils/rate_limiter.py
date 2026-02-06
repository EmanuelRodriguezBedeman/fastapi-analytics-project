import threading
import time
from collections import deque
from typing import Dict

from fastapi import HTTPException, Request, status


class RateLimiter:
    """
    In-memory rate limiter with rolling window logic.
    Supports multiple windows (e.g., minute and hour).
    """

    def __init__(self, limits: Dict[int, int]):
        """
        limits: Dict mapping window size (seconds) to max requests.
        Example: {60: 30, 3600: 300}
        """
        self.limits = limits
        # Using a lock for thread safety since counters are in-memory
        self.lock = threading.Lock()
        # Storage: {ip: {window_seconds: deque([timestamps])}}
        self.history: Dict[str, Dict[int, deque]] = {}

    def is_rate_limited(self, ip: str) -> bool:
        """
        Main logic to check if an IP has exceeded any of the defined limits.
        """
        now = time.time()

        with self.lock:
            if ip not in self.history:
                self.history[ip] = {window: deque() for window in self.limits}

            client_history = self.history[ip]

            # Check each window
            for window_seconds, max_requests in self.limits.items():
                timestamps = client_history[window_seconds]

                # Cleanup old timestamps
                while timestamps and timestamps[0] < now - window_seconds:
                    timestamps.popleft()

                # Check if limited
                if len(timestamps) >= max_requests:
                    return True

            # If not limited in any window, record this request in all windows
            for window_seconds in self.limits:
                client_history[window_seconds].append(now)

            return False


# Limits: 30 per 60s, 300 per 3600s
limiter = RateLimiter(limits={60: 30, 3600: 300})


async def rate_limit_dependency(request: Request):
    """
    FastAPI dependency to be used globally.
    """
    # Try to get IP from X-Forwarded-For (proxies like Render/Nginx)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    else:
        # Fallback to direct client host
        client_ip = request.client.host if request.client else "unknown"

    if limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )
