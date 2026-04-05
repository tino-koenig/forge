from __future__ import annotations

import unittest

from core.runtime_settings_foundation_registry import SettingSpec


class RuntimeSettingsFoundationRegistryTests(unittest.TestCase):
    def test_valid_specs_are_constructible(self) -> None:
        enum_spec = SettingSpec(
            key="x.mode",
            kind="enum",
            default="fast",
            allowed_values=("fast", "slow"),
            normalize=("strip", "lowercase"),
        )
        self.assertEqual(enum_spec.default, "fast")

        numeric_spec = SettingSpec(
            key="x.max",
            kind="int",
            default=10,
            min=1,
            max=20,
        )
        self.assertEqual(numeric_spec.default, 10)

    def test_invalid_enum_specs_fail(self) -> None:
        with self.assertRaises(ValueError):
            SettingSpec(
                key="x.mode",
                kind="enum",
                default="fast",
                allowed_values=None,
            )

        with self.assertRaises(ValueError):
            SettingSpec(
                key="x.mode",
                kind="enum",
                default="medium",
                allowed_values=("fast", "slow"),
            )

    def test_invalid_normalize_usage_fails(self) -> None:
        with self.assertRaises(ValueError):
            SettingSpec(
                key="x.enabled",
                kind="bool",
                default=True,
                normalize=("strip",),
            )

    def test_invalid_min_max_combinations_fail(self) -> None:
        with self.assertRaises(ValueError):
            SettingSpec(
                key="x.threshold",
                kind="float",
                default=0.5,
                min=1.0,
                max=0.0,
            )

        with self.assertRaises(ValueError):
            SettingSpec(
                key="x.note",
                kind="str",
                default="ok",
                min=1,
            )

    def test_bool_is_not_accepted_as_int_default(self) -> None:
        with self.assertRaises(ValueError):
            SettingSpec(
                key="x.count",
                kind="int",
                default=True,
                min=0,
                max=5,
            )

    def test_default_out_of_bounds_fails(self) -> None:
        with self.assertRaises(ValueError):
            SettingSpec(
                key="x.max",
                kind="int",
                default=100,
                min=1,
                max=10,
            )


if __name__ == "__main__":
    unittest.main()
