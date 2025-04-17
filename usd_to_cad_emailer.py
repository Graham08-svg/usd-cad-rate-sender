import requests
import csv
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

# Settings
API_URL = "https://api.frankfurter.app/latest?from=USD&to=CAD"
CSV_FILENAME = "usd_to_cad_history.csv"
from dotenv import load_dotenv
load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# Step 1: Get the rate
resp = requests.get(API_URL)
data = resp.json()
date = data['date']
rate = data['rates']['CAD']

# Step 2: Append to CSV only if new
file_exists = os.path.isfile(CSV_FILENAME)
should_append = True

if file_exists:
    with open(CSV_FILENAME, 'r') as f:
        reader = list(csv.reader(f))
        if reader and reader[-1][0] == date:
            should_append = False

if should_append:
    with open(CSV_FILENAME, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "USD_to_CAD"])
        writer.writerow([date, rate])

# Step 3: Email it
msg = EmailMessage()
msg["Subject"] = "USD to CAD Exchange Rate History"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO
msg.set_content(f"Attached is your running history of USD to CAD rates.\nLatest: {date} = {rate}")

with open(CSV_FILENAME, "rb") as f:
    msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=CSV_FILENAME)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_FROM, APP_PASSWORD)
    smtp.send_message(msg)

print(f"Sent {CSV_FILENAME} with latest rate {rate} on {date}")
