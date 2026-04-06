from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from scripts.run_quality_gates import (
    GateError,
    _extract_mypy_error_count,
    gate_repo_wide_mypy_baseline,
)


class RepoWideMypyBaselineGateTests(unittest.TestCase):
    def test_extract_mypy_error_count_from_summary(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["mypy"],
            returncode=1,
            stdout="Found 206 errors in 22 files (checked 80 source files)\n",
            stderr="",
        )
        self.assertEqual(_extract_mypy_error_count(proc), 206)

    def test_extract_mypy_error_count_falls_back_to_error_lines(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["mypy"],
            returncode=1,
            stdout="core/a.py:10: error: bad\nmodes/b.py:12: error: bad\n",
            stderr="",
        )
        self.assertEqual(_extract_mypy_error_count(proc), 2)

    @patch("scripts.run_quality_gates._select_mypy_command", return_value=["python", "-m", "mypy"])
    @patch("scripts.run_quality_gates.run_cmd")
    def test_repo_wide_mypy_baseline_allows_at_baseline(self, run_cmd_mock, _) -> None:
        run_cmd_mock.return_value = subprocess.CompletedProcess(
            args=["python", "-m", "mypy"],
            returncode=1,
            stdout="Found 206 errors in 22 files (checked 80 source files)\n",
            stderr="",
        )
        gate_repo_wide_mypy_baseline()

    @patch("scripts.run_quality_gates._select_mypy_command", return_value=["python", "-m", "mypy"])
    @patch("scripts.run_quality_gates.run_cmd")
    def test_repo_wide_mypy_baseline_rejects_regression(self, run_cmd_mock, _) -> None:
        run_cmd_mock.return_value = subprocess.CompletedProcess(
            args=["python", "-m", "mypy"],
            returncode=1,
            stdout="Found 207 errors in 22 files (checked 80 source files)\n",
            stderr="",
        )
        with self.assertRaises(GateError):
            gate_repo_wide_mypy_baseline()


if __name__ == "__main__":
    unittest.main()
