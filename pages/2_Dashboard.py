import streamlit as st
import pandas as pd
import plotly.express as px

from utils.database import init_db, fetch_all_complaints

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
init_db()

st.title("📊 Complaint Analytics Dashboard")

df = fetch_all_complaints()

if df.empty:
    st.info("No complaints yet. Go to Submit Complaint to add some.")
    st.stop()

df["datetime_parsed"] = pd.to_datetime(df["datetime"], errors="coerce")
df["date_only"] = df["datetime_parsed"].dt.date

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Complaints", len(df))
col2.metric("High Priority", int((df["priority"] == "High").sum()))
col3.metric("Pending", int((df["status"] == "Pending").sum()))
col4.metric("Resolved", int((df["status"] == "Resolved").sum()))

st.markdown("---")

st.subheader("Complaints by Category")
cat_counts = df["category"].value_counts().reset_index()
cat_counts.columns = ["Category", "Count"]
fig_cat = px.bar(cat_counts, x="Category", y="Count", color="Category")
st.plotly_chart(fig_cat, use_container_width=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Complaints by Priority")
    pri_counts = df["priority"].value_counts().reset_index()
    pri_counts.columns = ["Priority", "Count"]
    fig_pri = px.pie(pri_counts, names="Priority", values="Count")
    st.plotly_chart(fig_pri, use_container_width=True)

with chart_col2:
    st.subheader("Complaints by Station")
    station_counts = df["station"].value_counts().reset_index()
    station_counts.columns = ["Station", "Count"]
    fig_station = px.bar(station_counts, x="Count", y="Station", orientation="h")
    st.plotly_chart(fig_station, use_container_width=True)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("Complaints by Sentiment")
    sent_counts = df["sentiment"].value_counts().reset_index()
    sent_counts.columns = ["Sentiment", "Count"]
    color_map = {"Positive": "#2ecc71", "Neutral": "#95a5a6", "Negative": "#e74c3c"}
    fig_sent = px.pie(sent_counts, names="Sentiment", values="Count",
                       color="Sentiment", color_discrete_map=color_map)
    st.plotly_chart(fig_sent, use_container_width=True)

st.subheader("Complaints Over Time")
time_counts = df.groupby("date_only").size().reset_index(name="Count")
fig_time = px.line(time_counts, x="date_only", y="Count", markers=True)
st.plotly_chart(fig_time, use_container_width=True)

st.markdown("---")

st.subheader("🔴 High Priority Complaints")
high_priority = df[df["priority"] == "High"][
    ["complaint_id", "station", "category", "summary", "status"]
]
if high_priority.empty:
    st.success("No high-priority complaints. ✅")
else:
    st.dataframe(high_priority, use_container_width=True, hide_index=True)

st.subheader("Recent Complaints")
recent = df[["complaint_id", "datetime", "station", "category", "priority", "status"]].head(10)
st.dataframe(recent, use_container_width=True, hide_index=True)