from __future__ import annotations

import unittest
from pathlib import Path

from core.toml_compat import tomli


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"


class FixturePythonpathConfigurationTests(unittest.TestCase):
    def test_pytest_configuration_includes_basic_fixture_pythonpath(self) -> None:
        payload = tomli.loads(PYPROJECT.read_text(encoding="utf-8"))
        tool = payload.get("tool", {})
        self.assertIsInstance(tool, dict)

        pytest_config = tool.get("pytest", {}).get("ini_options", {})
        self.assertIsInstance(pytest_config, dict)

        pythonpath = pytest_config.get("pythonpath")
        self.assertEqual(pythonpath, ["tests/fixtures/basic_repo"])

        norecursedirs = pytest_config.get("norecursedirs")
        self.assertIsInstance(norecursedirs, list)
        self.assertIn("mutants", norecursedirs)


if __name__ == "__main__":
    unittest.main()
