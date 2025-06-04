- **app.py**
```python
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from src.config import load_config
from src.db import DB


@st.cache_data(ttl=10)
def load_data(limit: int = 1000):
    config = load_config()
    db = DB.create(config.db_path, config.backup_dir)
    rows = db.fetch_entries(limit)
    df = pd.DataFrame(
        rows,
        columns=[
            "id",
            "type",
            "text",
            "subreddit",
            "author",
            "created_utc",
            "score",
            "matched_terms",
            "url",
        ],
    )
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s", utc=True)
    df["created_local"] = df["created_utc"].dt.tz_convert("Europe/Berlin")
    return df


def main() -> None:
    st.set_page_config(page_title="Reddit Right-Wing Monitor", layout="wide")
    st.title("Right-Wing Reddit Monitor")

    df = load_data()
    last_refresh = st.session_state.get("last_refresh", datetime.utcnow())
    new_items = df[df["created_utc"] > last_refresh]
    st.session_state["last_refresh"] = datetime.utcnow()

    st.markdown(f"**Neue Treffer seit letztem Refresh:** {len(new_items)}")

    search = st.text_input("Suche")
    if search:
        df = df[df["text"].str.contains(search, case=False, na=False)]

    st.dataframe(
        df[
            [
                "text",
                "subreddit",
                "author",
                "created_utc",
                "created_local",
                "score",
                "matched_terms",
                "url",
            ]
        ]
    )

    if not df.empty:
        hourly = df.set_index("created_utc").resample("1H").size()
        st.line_chart(hourly)


if __name__ == "__main__":
    main()
