from __future__ import annotations

import unittest

from core.runtime_settings_foundation import (
    CODE_DEFAULT_FALLBACK_BLOCKED,
    CODE_INVALID_DEFAULT,
    CODE_INVALID_TYPE,
    CODE_OUT_OF_BOUNDS,
    CODE_UNKNOWN_ENUM_VALUE,
    CODE_UNKNOWN_KEY,
    resolve_setting,
    resolve_settings,
)
from core.runtime_settings_foundation_registry import SettingSpec


class RuntimeSettingsFoundationTests(unittest.TestCase):
    def test_source_priority_cli_over_local_over_repo_over_default(self) -> None:
        sources = {
            "repo": {"analysis.max_files": 100},
            "local": {"analysis.max_files": 200},
            "cli": {"analysis.max_files": 300},
        }
        resolved = resolve_setting("analysis.max_files", sources)
        self.assertEqual(resolved.value, 300)
        self.assertEqual(resolved.source, "cli")
        self.assertEqual(resolved.diagnostics, tuple())

    def test_invalid_input_falls_back_to_lower_source(self) -> None:
        sources = {
            "repo": {"analysis.max_files": 220},
            "local": {"analysis.max_files": "invalid"},
            "cli": {"analysis.max_files": "also-invalid"},
        }
        resolved = resolve_setting("analysis.max_files", sources)
        self.assertEqual(resolved.value, 220)
        self.assertEqual(resolved.source, "repo")
        self.assertEqual(len(resolved.diagnostics), 2)
        self.assertEqual(resolved.diagnostics[0].code, CODE_INVALID_TYPE)
        self.assertEqual(resolved.diagnostics[0].source, "cli")
        self.assertEqual(resolved.diagnostics[0].fallback_source, "local")
        self.assertEqual(resolved.diagnostics[1].fallback_source, "repo")

    def test_fallback_source_targets_next_source_with_key(self) -> None:
        sources = {
            "repo": {"analysis.max_files": 220},
            "local": {"analysis.mode": "fast"},
            "cli": {"analysis.max_files": "not-an-int"},
        }
        resolved = resolve_setting("analysis.max_files", sources)
        self.assertEqual(resolved.value, 220)
        self.assertEqual(resolved.source, "repo")
        self.assertEqual(len(resolved.diagnostics), 1)
        self.assertEqual(resolved.diagnostics[0].code, CODE_INVALID_TYPE)
        self.assertEqual(resolved.diagnostics[0].fallback_source, "repo")

    def test_unknown_key_is_diagnosed(self) -> None:
        sources = {
            "cli": {"unknown.setting": 1},
        }
        resolved = resolve_setting("unknown.setting", sources)
        self.assertIsNone(resolved.value)
        self.assertEqual(resolved.source, "default")
        self.assertEqual(len(resolved.diagnostics), 1)
        self.assertEqual(resolved.diagnostics[0].code, CODE_UNKNOWN_KEY)
        self.assertEqual(resolved.diagnostics[0].source, "cli")

    def test_unknown_key_without_occurrence_uses_consistent_source(self) -> None:
        resolved = resolve_setting("unknown.setting", {})
        self.assertIsNone(resolved.value)
        self.assertEqual(resolved.source, "default")
        self.assertEqual(len(resolved.diagnostics), 1)
        self.assertEqual(resolved.diagnostics[0].code, CODE_UNKNOWN_KEY)
        self.assertEqual(resolved.diagnostics[0].source, "default")

    def test_bound_validation_and_default_fallback(self) -> None:
        sources = {
            "cli": {"analysis.max_files": 99999},
            "local": {"analysis.max_files": -1},
        }
        resolved = resolve_setting("analysis.max_files", sources)
        self.assertEqual(resolved.value, 50)
        self.assertEqual(resolved.source, "default")
        self.assertEqual([d.code for d in resolved.diagnostics], [CODE_OUT_OF_BOUNDS, CODE_OUT_OF_BOUNDS])

    def test_enum_validation(self) -> None:
        sources = {
            "cli": {"analysis.mode": "invalid"},
            "repo": {"analysis.mode": " deep "},
        }
        resolved = resolve_setting("analysis.mode", sources)
        self.assertEqual(resolved.value, "deep")
        self.assertEqual(resolved.source, "repo")
        self.assertEqual(len(resolved.diagnostics), 1)
        self.assertEqual(resolved.diagnostics[0].code, CODE_UNKNOWN_ENUM_VALUE)

    def test_default_fallback_can_be_disabled(self) -> None:
        registry = {
            "analysis.strict_value": SettingSpec(
                key="analysis.strict_value",
                kind="int",
                default=7,
                min=0,
                max=9,
                allow_default_fallback=False,
            )
        }
        sources = {
            "cli": {"analysis.strict_value": "oops"},
        }
        resolved = resolve_setting("analysis.strict_value", sources, registry)
        self.assertIsNone(resolved.value)
        self.assertEqual(resolved.source, "default")
        self.assertEqual(resolved.diagnostics[-1].code, CODE_DEFAULT_FALLBACK_BLOCKED)

    def test_invalid_default_is_diagnosed_and_not_silently_used(self) -> None:
        class _UnsafeSpec:
            def __init__(self) -> None:
                self.key = "analysis.bad_default"
                self.kind = "int"
                self.default = 100
                self.min = 0
                self.max = 10
                self.allowed_values = None
                self.normalize = tuple()
                self.allow_default_fallback = True

        registry = {
            "analysis.bad_default": _UnsafeSpec(),  # type: ignore[assignment]
        }
        resolved = resolve_setting("analysis.bad_default", {}, registry)
        self.assertIsNone(resolved.value)
        self.assertEqual(resolved.source, "default")
        self.assertEqual(len(resolved.diagnostics), 1)
        self.assertEqual(resolved.diagnostics[0].code, CODE_INVALID_DEFAULT)
        self.assertEqual(resolved.diagnostics[0].source, "default")

    def test_diagnostics_and_determinism_for_resolve_settings(self) -> None:
        keys = [
            "analysis.mode",
            "analysis.max_files",
            "analysis.mode",
            "unknown.setting",
        ]
        sources = {
            "cli": {
                "analysis.mode": "INVALID",
                "analysis.max_files": "bad",
                "unknown.setting": True,
            },
            "local": {
                "analysis.mode": "FAST",
                "analysis.max_files": 200,
            },
            "repo": {
                "analysis.mode": "standard",
                "analysis.max_files": 150,
            },
        }

        first = resolve_settings(keys, sources)
        second = resolve_settings(keys, sources)

        self.assertEqual(first, second)
        self.assertEqual(list(first.keys()), ["analysis.mode", "analysis.max_files", "unknown.setting"])
        self.assertEqual(first["analysis.mode"].value, "fast")
        self.assertEqual(first["analysis.mode"].source, "local")
        self.assertEqual(first["analysis.max_files"].value, 200)
        self.assertEqual(first["unknown.setting"].diagnostics[0].code, CODE_UNKNOWN_KEY)


if __name__ == "__main__":
    unittest.main()
