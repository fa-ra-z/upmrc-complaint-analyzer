import streamlit as st
from utils.database import init_db, fetch_all_complaints

st.set_page_config(page_title="UPMRC AI Complaint Analyzer", page_icon="🚇", layout="wide")
init_db()

st.title("🚇 AI Metro Complaint Analyzer — UPMRC Lucknow")
st.caption("Internship Project · Automated complaint classification, routing and analytics")

df = fetch_all_complaints()

col1, col2, col3 = st.columns(3)
col1.metric("Total Complaints Logged", len(df))
col2.metric("Pending", int((df["status"] == "Pending").sum()) if not df.empty else 0)
col3.metric("High Priority", int((df["priority"] == "High").sum()) if not df.empty else 0)

st.markdown("---")

st.subheader("How this project works")
st.markdown("""
1. **Submit Complaint** — a passenger complaint is typed into a form.
2. **AI Classification** — Gemini reads the text and returns category, sentiment, and urgency.
3. **Priority & Routing** — fixed Python rules decide priority level and which department handles it.
4. **Storage** — the complaint is saved to a SQLite database.
5. **Dashboard** — charts summarize all complaints for management.
6. **Fallback safety net** — if the AI API fails, a keyword-based classifier takes over automatically.

Use the sidebar to move between pages.
""")