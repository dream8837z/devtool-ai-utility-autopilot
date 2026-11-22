"""Unit & integration tests for ToolForge Pro autopilot."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from toolforge_engine.config import ToolForgeConfig
from toolforge_engine.pipeline import run_pipeline


class TestToolForgePipeline(unittest.TestCase):
    def test_full_build_and_audit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            cfg = ToolForgeConfig(
                site_name="ToolForge Pro",
                site_url="https://dream8837z.github.io/devtool-ai-utility-autopilot",
                host="dream8837z.github.io",
                root_portal_url="https://dream8837z.github.io/",
                kr_hub_url="https://dream8837z.github.io/pseo-revenue-autopilot/",
                wealthstack_url="https://dream8837z.github.io/passive-income-microsaas-autopilot/",
                adsense_client_id="ca-pub-9014872001634608",
                indexnow_key="toolforgeindexnowkey2026901487",
                enable_indexnow=False,
                contact_email="contact@toolforge.pro",
                dist_dir=Path(td) / "dist",
            )
            res = run_pipeline(cfg)
            self.assertEqual(res["audit"]["status"], "PASS")
            self.assertEqual(res["audit"]["error_count"], 0)
            self.assertEqual(res["audit"]["page_count"], 95)
            self.assertTrue((cfg.dist_dir / "llms.txt").exists())
            self.assertTrue((cfg.dist_dir / "feed.xml").exists())
            self.assertTrue((cfg.dist_dir / "toolforgeindexnowkey2026901487.txt").exists())


if __name__ == "__main__":
    unittest.main()
