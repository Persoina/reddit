from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime, timezone
from typing import Iterable, List

import asyncpraw

from .config import AppConfig, load_config
from .db import DB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_submission(submission: asyncpraw.models.Submission, config: AppConfig, db: DB) -> None:
    text = f"{submission.title}\n{submission.selftext}" if hasattr(submission, "selftext") else submission.title
    matched = match_terms(text, config.right_wing_terms)
    if submission.subreddit.display_name.lower() in [s.lower() for s in config.right_wing_subs] or matched:
        created = submission.created_utc
        db.insert_entry(
            entry_id=submission.id,
            entry_type="submission",
            text=text[:280],
            subreddit=submission.subreddit.display_name,
            author=str(submission.author),
            created_utc=created,
            score=submission.score,
            matched_terms=matched,
            url=f"https://www.reddit.com{submission.permalink}",
        )
        logger.info("Stored submission %s", submission.id)


def match_terms(text: str, terms: Iterable[str]) -> List[str]:
    matched = []
    for term in terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        if pattern.search(text):
            matched.append(term)
    return matched


async def handle_comment(comment: asyncpraw.models.Comment, config: AppConfig, db: DB) -> None:
    text = comment.body
    matched = match_terms(text, config.right_wing_terms)
    if comment.subreddit.display_name.lower() in [s.lower() for s in config.right_wing_subs] or matched:
        created = comment.created_utc
        db.insert_entry(
            entry_id=comment.id,
            entry_type="comment",
            text=text[:280],
            subreddit=comment.subreddit.display_name,
            author=str(comment.author),
            created_utc=created,
            score=comment.score,
            matched_terms=matched,
            url=f"https://www.reddit.com{comment.permalink}",
        )
        logger.info("Stored comment %s", comment.id)


async def monitor_submissions(reddit: asyncpraw.Reddit, config: AppConfig, db: DB) -> None:
    subreddit = await reddit.subreddit("+".join(config.right_wing_subs)) if config.right_wing_subs else await reddit.subreddit("all")
    while True:
        try:
            async for submission in subreddit.stream.submissions(skip_existing=True):
                await handle_submission(submission, config, db)
        except Exception as exc:  # noqa: BLE001
            logger.error("Error in submission stream: %s", exc)
            await asyncio.sleep(10)


async def monitor_comments(reddit: asyncpraw.Reddit, config: AppConfig, db: DB) -> None:
    subreddit = await reddit.subreddit("+".join(config.right_wing_subs)) if config.right_wing_subs else await reddit.subreddit("all")
    while True:
        try:
            async for comment in subreddit.stream.comments(skip_existing=True):
                await handle_comment(comment, config, db)
        except Exception as exc:  # noqa: BLE001
            logger.error("Error in comment stream: %s", exc)
            await asyncio.sleep(10)


async def main() -> None:
    config = load_config()
    db = DB.create(config.db_path, config.backup_dir)

    reddit = asyncpraw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )

    tasks = [
        asyncio.create_task(monitor_submissions(reddit, config, db)),
        asyncio.create_task(monitor_comments(reddit, config, db)),
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
