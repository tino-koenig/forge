"""Compatibility layer for TOML parsing across Python versions."""

from __future__ import annotations

try:  # Python 3.11+
    import tomllib as tomli  # type: ignore[no-redef]
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli  # type: ignore[no-redef]

