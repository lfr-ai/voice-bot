"""API middleware components."""

from ekko.presentation.api.middleware.authentication import AuthenticationMiddleware
from ekko.presentation.api.middleware.cors import setup_cors
from ekko.presentation.api.middleware.error_handler import register_error_handlers
from ekko.presentation.api.middleware.request_id import RequestIdMiddleware
from ekko.presentation.api.middleware.security_headers import SecurityHeadersMiddleware
from ekko.presentation.api.middleware.timing import TimingMiddleware

__all__ = [
    "AuthenticationMiddleware",
    "RequestIdMiddleware",
    "SecurityHeadersMiddleware",
    "TimingMiddleware",
    "register_error_handlers",
    "setup_cors",
]
