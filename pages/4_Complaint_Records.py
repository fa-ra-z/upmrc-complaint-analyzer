import streamlit as st
import pandas as pd

from utils.database import init_db, fetch_all_complaints, update_complaint_status

st.set_page_config(page_title="Complaint Records", page_icon="📋", layout="wide")
init_db()

st.title("📋 Complaint Records")

df = fetch_all_complaints()

if df.empty:
    st.info("No complaints yet.")
    st.stop()

search_col, station_col, status_col = st.columns(3)

with search_col:
    search_text = st.text_input("🔎 Search complaint text or ID")

with station_col:
    station_filter = st.selectbox("Station", ["All"] + sorted(df["station"].dropna().unique().tolist()))

with status_col:
    status_filter = st.selectbox("Status", ["All", "Pending", "In Progress", "Resolved"])

filtered = df.copy()

if search_text:
    mask = (
        filtered["complaint_text"].str.contains(search_text, case=False, na=False)
        | filtered["complaint_id"].str.contains(search_text, case=False, na=False)
    )
    filtered = filtered[mask]

if station_filter != "All":
    filtered = filtered[filtered["station"] == station_filter]

if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]

st.caption(f"Showing {len(filtered)} of {len(df)} total complaints")
st.dataframe(
    filtered[["complaint_id", "station", "category", "priority", "status", "summary"]],
    use_container_width=True, hide_index=True,
)

st.markdown("---")
st.subheader("Update Complaint Status")

selected_id = st.selectbox("Select Complaint ID", filtered["complaint_id"].tolist())

if selected_id:
    row = df[df["complaint_id"] == selected_id].iloc[0]

    st.write(f"**Complaint:** {row['complaint_text']}")
    st.write(f"**Station:** {row['station']} · **Category:** {row['category']} · **Priority:** {row['priority']}")

    new_status = st.selectbox(
        "New Status", ["Pending", "In Progress", "Resolved"],
        index=["Pending", "In Progress", "Resolved"].index(row["status"]),
    )

    if st.button("💾 Update Status"):
        update_complaint_status(selected_id, new_status)
        st.success(f"Status updated to '{new_status}' for {selected_id}.")
        st.rerun()