from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from dotenv import load_dotenv


@dataclass
class AppConfig:
    client_id: str
    client_secret: str
    user_agent: str
    right_wing_subs: List[str]
    right_wing_terms: List[str]
    db_path: Path = Path("monitoring.db")
    backup_dir: Path = Path("backups")


def load_config() -> AppConfig:
    load_dotenv()
    client_id = os.getenv("CLIENT_ID", "")
    client_secret = os.getenv("CLIENT_SECRET", "")
    user_agent = os.getenv("USER_AGENT", "reddit-monitor")

    with open("config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)
    subs = cfg.get("RIGHT_WING_SUBS", [])
    terms = cfg.get("RIGHT_WING_TERMS", [])

    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)

    return AppConfig(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        right_wing_subs=subs,
        right_wing_terms=terms,
        backup_dir=backup_dir,
    )
