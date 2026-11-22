"""Configuration for ToolForge Pro with Coupang Partners (AF9272027) & Release Vault."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ToolForgeConfig:
    site_name: str
    site_url: str
    host: str
    root_portal_url: str
    kr_hub_url: str
    wealthstack_url: str
    adsense_client_id: str
    indexnow_key: str
    enable_indexnow: bool
    contact_email: str
    dist_dir: Path
    affiliate_cloud_url: str = "https://link.coupang.com/a/iSVrev2q5s"
    affiliate_ai_url: str = "https://link.coupang.com/a/iSVpT5nClE"
    gumroad_vault_url: str = "https://github.com/dream8837z/devtool-ai-utility-autopilot/releases/download/v1.0.0/ToolForge_AI_Prompt_DevOps_Vault_v1.zip"
    chrome_ext_url: str = "https://github.com/dream8837z/devtool-ai-utility-autopilot/releases/download/v1.0.0/toolforge-pro-extension-v1.0.0.zip"
    coupang_partner_id: str = "AF9272027"

    @property
    def adsense_pub_id(self) -> str:
        cid = self.adsense_client_id.strip()
        return cid[3:] if cid.startswith("ca-") else cid


def load_config(project_root: Path | None = None) -> ToolForgeConfig:
    root = project_root or Path(__file__).resolve().parent.parent
    if not root.is_dir():
        root = Path.cwd()
    site_url = os.environ.get(
        "SITE_URL",
        "https://dream8837z.github.io/devtool-ai-utility-autopilot",
    ).rstrip("/")
    return ToolForgeConfig(
        site_name=os.environ.get(
            "SITE_NAME",
            "ToolForge Pro — Free Online DevTools, Cron, Regex & AI Prompt Utilities",
        ),
        site_url=site_url,
        host="dream8837z.github.io",
        root_portal_url=os.environ.get("ROOT_PORTAL_URL", "https://dream8837z.github.io/"),
        kr_hub_url=os.environ.get("KR_HUB_URL", "https://dream8837z.github.io/pseo-revenue-autopilot/"),
        wealthstack_url=os.environ.get(
            "WEALTHSTACK_URL",
            "https://dream8837z.github.io/passive-income-microsaas-autopilot/",
        ),
        adsense_client_id=os.environ.get("ADSENSE_CLIENT_ID", "ca-pub-9014872001634608"),
        indexnow_key=os.environ.get("INDEXNOW_KEY", "toolforgeindexnowkey2026901487"),
        enable_indexnow=os.environ.get("ENABLE_INDEXNOW", "false").lower() == "true",
        contact_email=os.environ.get("CONTACT_EMAIL", "contact@toolforge.pro"),
        dist_dir=root / "dist",
        affiliate_cloud_url=os.environ.get("AFFILIATE_CLOUD_URL", "").strip() or "https://link.coupang.com/a/iSVrev2q5s",
        affiliate_ai_url=os.environ.get("AFFILIATE_AI_URL", "").strip() or "https://link.coupang.com/a/iSVpT5nClE",
        gumroad_vault_url=os.environ.get("GUMROAD_VAULT_URL", "").strip() or "https://github.com/dream8837z/devtool-ai-utility-autopilot/releases/download/v1.0.0/ToolForge_AI_Prompt_DevOps_Vault_v1.zip",
        chrome_ext_url=os.environ.get("CHROME_EXT_URL", "").strip() or "https://github.com/dream8837z/devtool-ai-utility-autopilot/releases/download/v1.0.0/toolforge-pro-extension-v1.0.0.zip",
    )
