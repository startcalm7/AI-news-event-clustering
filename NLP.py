import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ---------- FILE PATH ----------
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
PARQUET_PATH = os.path.join(CURRENT_FOLDER, "your_cleaned_dataset.parquet")

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="News Event Explorer", layout="wide")
st.title("📰 News Event Detection & Timeline Dashboard")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data(path):
    return pd.read_parquet(path)

with st.spinner("Loading dataset..."):
    df = load_data(PARQUET_PATH)

# Clean date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

st.success(f"Dataset loaded: {df.shape[0]:,} articles")

# =========================================================
# SIDEBAR — PROPER CLUSTER SELECTION (FIXED)
# =========================================================
st.sidebar.header("🔎 Filter Events")

cluster_counts = df["event_cluster"].value_counts().sort_index()
all_clusters = list(cluster_counts.index)

selected_cluster = st.sidebar.selectbox(
    "Select an Event Cluster:",
    all_clusters,
    index=0
)

event_df = df[df["event_cluster"] == selected_cluster]

st.sidebar.write(f"**Total articles in this event:** {len(event_df):,}")

# =========================================================
# EVENT SUMMARY (DYNAMIC — CHANGES WITH CLUSTER)
# =========================================================
st.subheader(f"📌 Event Cluster {selected_cluster}")

st.info(f"""
🧠 **Event Label:**  
{event_df['event_label'].iloc[0]}

📄 **Articles:** {len(event_df):,}

🗓 **Time span:**  
{event_df['date'].min().date()}  →  {event_df['date'].max().date()}

🌐 **Top Sources:**  
{', '.join(event_df['source'].value_counts().head(5).index)}

📝 **Summary:**  
{event_df['event_summary'].iloc[0]}
""")

# =========================================================
# TIMELINE — TOP 3 EVENTS (NOW WORKS)
# =========================================================
st.subheader("📅 Timeline (Top 3 Major Events)")

top3_clusters = (
    df["event_cluster"]
    .value_counts()
    .head(3)
    .index
    .tolist()
)

timeline_df = (
    df[df["event_cluster"].isin(top3_clusters)]
    .groupby(["date", "event_cluster"])
    .size()
    .reset_index(name="num_articles")
)

fig = px.line(
    timeline_df,
    x="date",
    y="num_articles",
    color="event_cluster",
    title="News Activity Timeline (Top 3 Events)"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# VIEW ARTICLES INSIDE EVENT (WORKING)
# =========================================================
st.subheader("📰 Read Articles in this Event")

selected_article = st.selectbox(
    "Choose an article:",
    event_df["project_title"].unique()
)

article_row = event_df[
    event_df["project_title"] == selected_article
].iloc[0]

st.markdown(f"🔗 **Read full article:** [{selected_article}]({article_row['url']})")

st.write("📄 Article Preview:")
st.write(article_row["project_content"][:1500] + "...")

# =========================================================
# TIMELINE TABLE (SAMPLE VIEW)
# =========================================================
st.subheader("📋 Event Timeline (sample view)")
st.dataframe(
    event_df[["date","project_title","source","event_label","url"]]
    .sort_values("date")
    .head(500)
)
