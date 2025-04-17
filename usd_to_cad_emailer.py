import csv
import smtplib
import requests
from datetime import datetime
from email.message import EmailMessage

# === CONFIG ===
EMAIL_ADDRESS = "graham@goodship.io"
APP_PASSWORD = "bdsrmffefgqrcjbm"
CSV_FILE = "usd_to_cad_history.csv"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === FETCH DATA ===
def get_exchange_rate():
    url = "https://api.frankfurter.app/latest?from=USD&to=CAD"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    rate = data["rates"]["CAD"]
    date = data["date"]
    return date, rate

# === APPEND TO CSV ===
def append_to_csv(date, rate):
    header = ["date", "USD_to_CAD"]
    try:
        with open(CSV_FILE, "r", newline="") as f:
            pass
    except FileNotFoundError:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, rate])

# === EMAIL FILE ===
def send_email():
    msg = EmailMessage()
    msg["Subject"] = "Daily USD→CAD Exchange Rate CSV"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content("Attached is today's USD→CAD exchange rate CSV.")

    with open(CSV_FILE, "rb") as f:
        msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=CSV_FILE)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, APP_PASSWORD)
        smtp.send_message(msg)

# === RUN ===
if __name__ == "__main__":
    today, rate = get_exchange_rate()
    append_to_csv(today, rate)
    send_email()
