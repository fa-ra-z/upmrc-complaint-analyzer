import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import init_db, insert_complaint, generate_complaint_id
from utils.ai_classifier import classify_complaint

st.set_page_config(page_title="Bulk Upload", page_icon="📁", layout="wide")
init_db()

st.title("📁 Bulk Upload Complaints")
st.write("Upload a CSV file with columns: complaint_text, station (required), source, date (optional)")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    upload_df = pd.read_csv(uploaded_file)

    required_cols = {"complaint_text", "station"}
    missing = required_cols - set(upload_df.columns)

    if missing:
        st.error(f"CSV is missing required column(s): {', '.join(missing)}")
        st.stop()

    st.write(f"Found **{len(upload_df)}** complaints in the file.")
    st.dataframe(upload_df.head(5), use_container_width=True)

if st.button("🚀 Analyze & Save All", use_container_width=True):
        progress = st.progress(0, text="Starting...")
        results_preview = []

        for i, row in upload_df.iterrows():
            text = str(row.get("complaint_text", "")).strip()
            if not text:
                continue

            result = classify_complaint(text)

            complaint_id = generate_complaint_id()
            record = {
                "complaint_id": complaint_id,
                "datetime": str(row.get("date", datetime.now().isoformat(timespec="seconds"))),
                "station": row.get("station", "Unknown"),
                "complaint_text": text,
                "source": row.get("source", "Bulk Upload"),
                "category": result["category"],
                "sentiment": result["sentiment"],
                "priority": result["priority"],
                "department": result["department"],
                "summary": result["summary"],
                "status": "Pending",
            }
            insert_complaint(record)
            results_preview.append({**record, "classified_by": result["classified_by"]})

            progress.progress(
                (i + 1) / len(upload_df),
                text=f"Processed {i + 1} / {len(upload_df)} complaints...",
            )

        progress.empty()
        st.success(f"✅ Done! {len(results_preview)} complaints analyzed and saved.")

        preview_df = pd.DataFrame(results_preview)[
            ["complaint_id", "station", "category", "priority", "classified_by"]
        ]
        st.dataframe(preview_df, use_container_width=True, hide_index=True)