import csv
import random
from datetime import datetime, timedelta

STATIONS = [
    "CCS Airport", "Amausi", "Transport Nagar", "Krishna Nagar", "Alambagh",
    "Charbagh", "Hazratganj", "Hussainganj", "Sachivalaya", "Munshipulia",
    "Badshahnagar", "Vishwavidyalaya", "Durgapuri", "Mawaiya",
]

COMPLAINT_TEMPLATES = [
    "The platform at {station} station was very dirty with garbage lying near the benches.",
    "Waited more than 20 minutes for a train at {station} station during peak hours.",
    "A suspicious unattended bag was spotted near the entry gate of {station} station.",
    "My card balance was deducted twice for a single journey from {station} station.",
    "The escalator at {station} station has been out of order for the past 3 days.",
    "The security guard at {station} station was rude to an elderly passenger.",
    "No drinking water available at {station} station, the cooler is broken.",
    "Great experience, the staff at {station} station were very helpful today.",
]

def generate(n=60):
    rows = []
    start_date = datetime.now() - timedelta(days=30)

    for i in range(n):
        template = random.choice(COMPLAINT_TEMPLATES)
        station = random.choice(STATIONS)
        text = template.format(station=station)

        complaint_date = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(6, 22),
        )

        rows.append({
            "complaint_text": text,
            "station": station,
            "source": random.choice(["App", "Email", "Counter", "Social Media"]),
            "date": complaint_date.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return rows

if __name__ == "__main__":
    rows = generate(60)

    with open("data/sample_complaints.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["complaint_text", "station", "source", "date"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} complaints -> data/sample_complaints.csv")

