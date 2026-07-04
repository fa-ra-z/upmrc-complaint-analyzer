import sqlite3
import pandas as pd
import os
import uuid
from datetime import datetime

DB_PATH = os.path.join("data", "complaints.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id     TEXT PRIMARY KEY,
            datetime         TEXT,
            station          TEXT,
            complaint_text   TEXT,
            source           TEXT,
            category         TEXT,
            sentiment        TEXT,
            priority         TEXT,
            department       TEXT,
            summary          TEXT,
            status           TEXT,
            created_at       TEXT
        )
    """)
    conn.commit()
    conn.close()
    
def generate_complaint_id():
    return "UPMRC-" + uuid.uuid4().hex[:8].upper()

def insert_complaint(record):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints (
            complaint_id, datetime, station, complaint_text, source,
            category, sentiment, priority, department, summary, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.get("complaint_id"),
        record.get("datetime"),
        record.get("station"),
        record.get("complaint_text"),
        record.get("source", ""),
        record.get("category"),
        record.get("sentiment"),
        record.get("priority"),
        record.get("department"),
        record.get("summary"),
        record.get("status", "Pending"),
        datetime.now().isoformat(timespec="seconds"),
    ))
    conn.commit()
    conn.close()

def fetch_all_complaints():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM complaints ORDER BY created_at DESC", conn)
    conn.close()
    return df

def update_complaint_status(complaint_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE complaints SET status = ? WHERE complaint_id = ?",
        (new_status, complaint_id),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    init_db()

    test_record = {
        "complaint_id": generate_complaint_id(),
        "datetime": "2026-07-03T10:00:00",
        "station": "Hazratganj",
        "complaint_text": "Test complaint for database check",
        "source": "Test",
        "category": "Other",
        "sentiment": "Neutral",
        "priority": "Low",
        "department": "General Administration",
        "summary": "Test complaint",
    }
    insert_complaint(test_record)

    df = fetch_all_complaints()
    print(df)