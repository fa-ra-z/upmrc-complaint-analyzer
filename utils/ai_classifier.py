import requests
import json
import re
import streamlit as st

from utils.keyword_classifier import classify_with_keywords, DEPARTMENT_MAP, HIGH_PRIORITY_WORDS

SYSTEM_PROMPT = """You are a complaint-triage assistant for UPMRC (Uttar Pradesh Metro Rail Corporation).
Read the passenger complaint and respond with ONLY a valid JSON object, nothing else, in exactly this shape:

{
  "category": one of ["Cleanliness", "Delay", "Security", "Ticketing", "Escalator/Lift", "Staff Behavior", "Other"],
  "sentiment": "Positive" or "Neutral" or "Negative",
  "summary": "one short sentence summarizing the complaint"
}

Return ONLY the JSON object, no markdown formatting, no extra text."""

def classify_with_ai(complaint_text):
    api_key = st.secrets["GEMINI_API_KEY"]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {"parts": [{"text": SYSTEM_PROMPT + "\n\nComplaint: " + complaint_text}]}
        ]
    }

    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()

    data = response.json()
    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]

    # Gemini sometimes wraps JSON in ```json fences even when told not to — strip those
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    result = json.loads(cleaned)
    return result

def classify_complaint(complaint_text):
    try:
        ai_result = classify_with_ai(complaint_text)
        category = ai_result.get("category", "Other")
        sentiment = ai_result.get("sentiment", "Neutral")
        summary = ai_result.get("summary", complaint_text[:100])
        classified_by = "AI (Gemini)"
    except Exception:
        fallback = classify_with_keywords(complaint_text)
        return {**fallback, "summary": complaint_text[:100], "classified_by": "Keyword Fallback"}

    # Apply the SAME priority/department rules from Day 3, using the AI's category
    text_lower = complaint_text.lower()
    is_emergency = any(word in text_lower for word in HIGH_PRIORITY_WORDS)

    if is_emergency or category == "Security":
        priority = "High"
    elif category in ["Escalator/Lift", "Ticketing", "Staff Behavior", "Delay"]:
        priority = "Medium"
    else:
        priority = "Low"

    department = DEPARTMENT_MAP.get(category, "General Administration")

    return {
        "category": category,
        "sentiment": sentiment,
        "priority": priority,
        "department": department,
        "summary": summary,
        "classified_by": classified_by,
    }


if __name__ == "__main__":
    test = "The train floor was covered in food scraps and the smell was unbearable"
    result = classify_complaint(test)
    print(result)

    