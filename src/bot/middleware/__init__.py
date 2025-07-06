"""Middleware package for bot."""

from .auth import AuthMiddleware

__all__ = ["AuthMiddleware"]