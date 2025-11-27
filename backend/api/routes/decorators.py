"""Route decorators."""
from functools import wraps
from typing import Callable, TypeVar, cast

from flask import jsonify, g, request

from backend.utils.security import verify_admin_token

F = TypeVar("F", bound=Callable[..., object])


def require_admin(func: F) -> F:
    """Require a valid admin bearer token."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
        if not token:
            token = request.args.get("token")
        if not token:
            return jsonify({"error": "Authentication required."}), 401

        admin = verify_admin_token(token)
        if not admin:
            return jsonify({"error": "Invalid or expired token."}), 401

        g.current_admin = admin
        return func(*args, **kwargs)

    return cast(F, wrapper)
