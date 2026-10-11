"""
Phase 7 Hardening — Security middleware and utilities.

SSRF protections: block loopback, RFC-1918 private ranges, and unsafe schemes.
Rate limiting: token bucket per-IP on expensive endpoints.
"""

from __future__ import annotations

import ipaddress
import re
import time
from collections import defaultdict
from threading import Lock
from urllib.parse import urlparse

from fastapi import Request, HTTPException


# ---------------------------------------------------------------------------
# SSRF Protection
# ---------------------------------------------------------------------------

_PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("::1/128"),          # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),         # IPv6 ULA
    ipaddress.ip_network("fe80::/10"),        # IPv6 link-local
]

_ALLOWED_SCHEMES = {"https", "http"}
_MAX_URL_LENGTH = 2048
_MAX_REDIRECTS = 3


def validate_source_url(url: str) -> str:
    """
    Validate and sanitise a URL before fetching from an external source.

    Raises ValueError if the URL is unsafe (SSRF vector, bad scheme, private IP).
    Returns the sanitised URL on success.

    Rules:
    - Only http/https schemes allowed.
    - Block loopback (127.x, ::1) and private RFC-1918 ranges.
    - Block URLs longer than 2048 chars.
    """
    if not url or len(url) > _MAX_URL_LENGTH:
        raise ValueError(f"URL must be non-empty and ≤{_MAX_URL_LENGTH} characters.")

    parsed = urlparse(url)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"URL scheme '{parsed.scheme}' is not allowed. Only http/https are permitted.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must include a valid hostname.")

    # Block by hostname patterns
    if hostname.lower() in ("localhost", "local"):
        raise ValueError(f"SSRF protection: hostname '{hostname}' is not allowed.")

    # Attempt IP resolution (for direct IP URLs only)
    try:
        addr = ipaddress.ip_address(hostname)
        for net in _PRIVATE_RANGES:
            if addr in net:
                raise ValueError(
                    f"SSRF protection: IP address {addr} is in a private/reserved range."
                )
    except ValueError as e:
        if "SSRF" in str(e):
            raise
        # hostname is a domain name, not an IP — pass through
        # Runtime DNS resolution safety must be enforced at the HTTP client level
        pass

    return url


# ---------------------------------------------------------------------------
# Simple in-memory rate limiter (token bucket)
# ---------------------------------------------------------------------------

class _TokenBucket:
    """Per-key token bucket for rate limiting."""

    def __init__(self, rate: float, capacity: int) -> None:
        self.rate = rate        # tokens per second
        self.capacity = capacity
        self._buckets: dict[str, tuple[float, float]] = defaultdict(lambda: (capacity, time.monotonic()))
        self._lock = Lock()

    def consume(self, key: str, tokens: int = 1) -> bool:
        """Returns True if request is allowed, False if rate limited."""
        with self._lock:
            available, last_refill = self._buckets[key]
            now = time.monotonic()
            elapsed = now - last_refill
            available = min(self.capacity, available + elapsed * self.rate)
            if available >= tokens:
                self._buckets[key] = (available - tokens, now)
                return True
            self._buckets[key] = (available, now)
            return False


# Shared rate limiters for expensive endpoints
_ai_limiter = _TokenBucket(rate=0.5, capacity=5)      # 0.5 req/s, burst 5
_compare_limiter = _TokenBucket(rate=1.0, capacity=10) # 1 req/s, burst 10


def check_ai_rate_limit(request: Request) -> None:
    """FastAPI dependency: rate-limit the AI assistant endpoint."""
    client_ip = request.client.host if request.client else "unknown"
    if not _ai_limiter.consume(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests to the AI assistant. Please wait a moment.",
            headers={"Retry-After": "2"},
        )


def check_compare_rate_limit(request: Request) -> None:
    """FastAPI dependency: rate-limit the comparison endpoint."""
    client_ip = request.client.host if request.client else "unknown"
    if not _compare_limiter.consume(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many comparison requests. Please wait a moment.",
            headers={"Retry-After": "1"},
        )
