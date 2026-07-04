from utils.ai_classifier import classify_complaint
from utils.database import init_db, insert_complaint, generate_complaint_id
from datetime import datetime

import streamlit as st
init_db()

st.title("Submit a Complaint")

with st.form("complaint_form"):
    complaint_text = st.text_area("Complaint Text")
    station = st.selectbox("Station", ["Charbagh", "Hazratganj", "Munshipulia", "Alambagh"])
    source = st.selectbox("Complaint Source", ["App", "Email", "Counter", "Social Media"])
    passenger_name = st.text_input("Passenger Name (optional)")

    submitted = st.form_submit_button("Submit Complaint")

if submitted:
    if not complaint_text.strip():
        st.error("Please enter the complaint text before submitting.")
    else:
        with st.spinner("Analyzing complaint..."):
            result = classify_complaint(complaint_text)

        complaint_id = generate_complaint_id()
        record = {
            "complaint_id": complaint_id,
            "datetime": datetime.now().isoformat(timespec="seconds"),
            "station": station,
            "complaint_text": complaint_text,
            "source": source,
            "category": result["category"],
            "sentiment": result["sentiment"],
            "priority": result["priority"],
            "department": result["department"],
            "summary": result["summary"],
            "status": "Pending",
        }
        insert_complaint(record)

        st.success(f"Complaint saved! ID: {complaint_id}")

        col1, col2 = st.columns(2)
        col1.metric("Sentiment", result["sentiment"])
        col2.metric("Priority", result["priority"])

        st.write(f"**Category:** {result['category']}")
        st.write(f"**Routed To:** {result['department']}")

        st.caption(f"Classified by: {result['classified_by']}")