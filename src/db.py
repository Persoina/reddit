from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Tuple


@dataclass
class DB:
    conn: sqlite3.Connection
    backup_dir: Path

    @classmethod
    def create(cls, db_path: Path, backup_dir: Path) -> "DB":
        conn = sqlite3.connect(db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entries (
                id TEXT PRIMARY KEY,
                type TEXT,
                text TEXT,
                subreddit TEXT,
                author TEXT,
                created_utc REAL,
                score INTEGER,
                matched_terms TEXT,
                url TEXT
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_created ON entries(created_utc)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subreddit ON entries(subreddit)")
        conn.commit()
        return cls(conn, backup_dir)

    def insert_entry(
        self,
        entry_id: str,
        entry_type: str,
        text: str,
        subreddit: str,
        author: str,
        created_utc: float,
        score: int,
        matched_terms: Iterable[str],
        url: str,
    ) -> None:
        terms = ",".join(matched_terms)
        self.conn.execute(
            """INSERT OR IGNORE INTO entries
            (id, type, text, subreddit, author, created_utc, score, matched_terms, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                entry_id,
                entry_type,
                text,
                subreddit,
                author,
                created_utc,
                score,
                terms,
                url,
            ),
        )
        self.conn.commit()
        self._backup_to_csv(
            entry_id,
            entry_type,
            text,
            subreddit,
            author,
            created_utc,
            score,
            terms,
            url,
        )

    def _backup_to_csv(
        self,
        entry_id: str,
        entry_type: str,
        text: str,
        subreddit: str,
        author: str,
        created_utc: float,
        score: int,
        terms: str,
        url: str,
    ) -> None:
        date = datetime.utcfromtimestamp(created_utc).strftime("%Y-%m-%d")
        path = self.backup_dir / f"{date}_monitoring.csv"
        write_header = not path.exists()
        with path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(
                    [
                        "id",
                        "type",
                        "text",
                        "subreddit",
                        "author",
                        "created_utc",
                        "score",
                        "matched_terms",
                        "url",
                    ]
                )
            writer.writerow(
                [
                    entry_id,
                    entry_type,
                    text,
                    subreddit,
                    author,
                    created_utc,
                    score,
                    terms,
                    url,
                ]
            )

    def fetch_entries(self, limit: int = 100) -> Iterable[Tuple]:
        cursor = self.conn.execute(
            "SELECT id, type, text, subreddit, author, created_utc, score, matched_terms, url FROM entries ORDER BY created_utc DESC LIMIT ?",
            (limit,),
        )
        return cursor.fetchall()
