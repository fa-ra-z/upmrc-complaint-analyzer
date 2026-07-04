CATEGORY_KEYWORDS = {
    "Cleanliness": ["dirty", "garbage", "smell", "unclean", "toilet", "litter"],
    "Delay": ["late", "delay", "waiting", "wait", "slow", "schedule"],
    "Security": ["theft", "harassment", "suspicious", "fire", "weapon", "accident"],
    "Ticketing": ["card", "token", "recharge", "ticket", "fare", "refund"],
    "Escalator/Lift": ["lift", "escalator", "elevator", "not working", "stuck"],
    "Staff Behavior": ["rude", "staff", "guard", "misbehave", "impolite"],
}

NEGATIVE_WORDS = ["bad", "worst", "poor", "terrible", "angry", "rude", "broken", "dirty", "late", "never"]
POSITIVE_WORDS = ["good", "great", "excellent", "clean", "helpful", "thank", "nice", "smooth"]

DEPARTMENT_MAP = {
    "Cleanliness": "Housekeeping Department",
    "Delay": "Operations Department",
    "Security": "Security Department",
    "Ticketing": "AFC/Ticketing Department",
    "Escalator/Lift": "Maintenance Department",
    "Staff Behavior": "Customer Service/HR",
    "Other": "General Administration",
}

HIGH_PRIORITY_WORDS = ["fire", "weapon", "harassment", "theft", "accident", "suspicious", "medical emergency"]

def classify_with_keywords(text):
    text_lower = text.lower()

    # --- Category detection (same as before) ---
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        count = 0
        for word in keywords:
            if word in text_lower:
                count += 1
        scores[category] = count

    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        best_category = "Other"

    # --- Sentiment detection ---
    neg_count = 0
    for word in NEGATIVE_WORDS:
        if word in text_lower:
            neg_count += 1

    pos_count = 0
    for word in POSITIVE_WORDS:
        if word in text_lower:
            pos_count += 1

    if neg_count > pos_count:
        sentiment = "Negative"
    elif pos_count > neg_count:
        sentiment = "Positive"
    else:
        sentiment = "Neutral"

    # --- Priority detection ---
    is_emergency = False
    for word in HIGH_PRIORITY_WORDS:
        if word in text_lower:
            is_emergency = True

    if is_emergency or best_category == "Security":
        priority = "High"
    elif best_category in ["Escalator/Lift", "Ticketing", "Staff Behavior", "Delay"]:
        priority = "Medium"
    else:
        priority = "Low"

    # --- Department routing ---
    department = DEPARTMENT_MAP.get(best_category, "General Administration")

    # --- Return everything as one dictionary ---
    return {
        "category": best_category,
        "sentiment": sentiment,
        "priority": priority,
        "department": department,
    }


if __name__ == "__main__":
    test1 = "The escalator at Hazratganj station is not working"
    test2 = "Staff member was very rude to me at the counter"
    test3 = "Great service today, very clean train"
    test4 = "There is a suspicious bag left near the gate"

    for t in [test1, test2, test3, test4]:
        result = classify_with_keywords(t)
        print(t)
        print(" ->", result)
        print()

