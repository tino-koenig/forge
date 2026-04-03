"""Compatibility executable module.

Preferred invocation is now:
- `forge ...` (console script from editable install)
- `python -m forge ...` (module invocation)

This file remains for backward compatibility with existing scripts.
"""

from __future__ import annotations

import sys

from forge.__main__ import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
