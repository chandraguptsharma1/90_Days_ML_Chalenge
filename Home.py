# Home.py
import json, os
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="90 Days ML + AI — Home", layout="wide")
ROOT = Path(__file__).resolve().parent
PROGRESS_FILE = ROOT / "progress.json"

# --- load/save progress ---
def load_progress():
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_progress(state):
    PROGRESS_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

progress = load_progress()  # {"1": true, "2": false, ...}

st.title("🚀 90 Days ML + AI — Challenge Hub")
st.caption("Select a day to open its app. Mark days complete as you go.")

# Define days shown on Home (add more as you create them)
DAYS = [
    {"num": 1, "title": "Matrix Art (Lite)", "page": "pages/Day1_MatrixArtGenerator.py", "icon": "🎨"},
    {"num": 2, "title": "Movie Dataset Explorer", "page": "pages/Day2_MovieDatasetExplorer.py", "icon": "🎬"},
    # append future days here...
]

# Stats
done = sum(1 for d in DAYS if progress.get(str(d["num"])) is True)
st.metric("Progress", f"{done} / {len(DAYS)} days")

st.divider()

# Grid of “cards”
cols = st.columns(3)
for i, d in enumerate(DAYS):
    with cols[i % 3]:
        st.subheader(f'{d["icon"]} Day {d["num"]}: {d["title"]}')
        st.page_link(d["page"], label="Open UI →", help=f"Open Day {d['num']} app", icon="↗️")
        # toggle complete
        key = f"done_{d['num']}"
        checked = st.checkbox("Mark complete", key=key, value=progress.get(str(d["num"]), False))
        if checked != progress.get(str(d["num"]), False):
            progress[str(d["num"])] = checked
            save_progress(progress)
            st.success("Progress saved.", icon="💾")

st.info("Add new days by dropping files into the **pages/** folder (e.g., `03_Day3_*.py`). They will auto‑appear here and in the sidebar.")
