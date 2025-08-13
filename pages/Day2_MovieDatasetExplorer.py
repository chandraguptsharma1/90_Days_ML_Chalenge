import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Day-2 Movie Explorer" , layout="wide")

#Load dataset
DATA_PATH = "data/movies_sample.csv"
if not os.path.exists(DATA_PATH):
    st.error(f"Dataset not found at {DATA_PATH}")
    st.stop()

df = pd.read_csv(DATA_PATH)

# --- Normalize column names & types (robust) ---
df.columns = [c.strip().lower() for c in df.columns]  # title, year, rating, genre, votes
df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["votes"] = pd.to_numeric(df.get("votes", 0), errors="coerce").fillna(0).astype(int)

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    years = st.slider("Year range", int(df["year"].min()), int(df["year"].max()), (2000, 2020))
    min_rating = st.slider("Minimum rating", float(df["rating"].min()), float(df["rating"].max()), 8.0)
    # build genre list
    genres = sorted({g.strip() for sub in df["genre"].dropna() for g in str(sub).split("|") if g.strip()})
    selected_genres = st.multiselect("Genres", genres)
    sort_by = st.selectbox("Sort by", ["rating", "votes"])
    top_n = st.slider("Top N movies", 5, 20, 10)

# Apply filters
mask = (df["year"].between(years[0], years[1])) & (df["rating"] >= min_rating)
if selected_genres:
    mask &= df["genre"].fillna("").apply(lambda g: any(genre in str(g) for genre in selected_genres))

filtered = df[mask].sort_values(sort_by, ascending=False).head(top_n)

# Show table
st.title("🎬 Day‑2: Movie Dataset Explorer")
st.dataframe(filtered[["title", "year", "rating", "genre", "votes"]], use_container_width=True)

# Plot chart (this was missing)
st.subheader(f"Top {len(filtered)} by {sort_by.capitalize()}")
if filtered.empty:
    st.info("No movies match the filters.")
else:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(filtered["title"][::-1], filtered[sort_by][::-1])
    ax.set_xlabel(sort_by.capitalize())
    ax.set_ylabel("Movie Title")
    plt.tight_layout()
    st.pyplot(fig)

# Export
if not filtered.empty:
    st.download_button(
        "⬇️ Download CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_movies.csv",
        mime="text/csv",
    )
