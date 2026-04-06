from __future__ import annotations

from types import SimpleNamespace
import unittest

from core.protocol_analytics_foundation import apply_filters


class ProtocolAnalyticsFoundationTests(unittest.TestCase):
    def _args(self, **overrides: object) -> SimpleNamespace:
        base = {
            "since": None,
            "until": None,
            "logs_run_id": None,
            "logs_capability": None,
            "logs_step_type": None,
            "logs_status": None,
            "logs_provider": None,
            "logs_model": None,
        }
        base.update(overrides)
        return SimpleNamespace(**base)

    def test_apply_filters_accepts_valid_logs_run_id(self) -> None:
        events = [
            {"run_id": 1, "timestamp": "2026-04-06T10:00:00Z"},
            {"run_id": 2, "timestamp": "2026-04-06T10:00:01Z"},
            {"run_id": "2", "timestamp": "2026-04-06T10:00:02Z"},
        ]
        filtered = apply_filters(events, self._args(logs_run_id="2"))
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(str(item.get("run_id")) == "2" for item in filtered))

    def test_apply_filters_rejects_invalid_logs_run_id(self) -> None:
        events = [{"run_id": 1, "timestamp": "2026-04-06T10:00:00Z"}]
        with self.assertRaises(ValueError) as exc:
            apply_filters(events, self._args(logs_run_id="abc"))
        self.assertIn("invalid --run-id filter", str(exc.exception))


if __name__ == "__main__":
    unittest.main()

