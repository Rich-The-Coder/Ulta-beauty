import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

OUTLOOK_EMAIL = os.getenv("OUTLOOK_EMAIL")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
SMS_EMAIL = os.getenv("SMS_EMAIL")

EMAIL_SUBJECT = "Ulta Beauty Reminder"
TARGET_DATE = "2025-12-28"


def send_email(body: str) -> None:
    missing = []
    if not OUTLOOK_EMAIL:
        missing.append("OUTLOOK_EMAIL")
    if not OUTLOOK_PASSWORD:
        missing.append("OUTLOOK_PASSWORD")
    if not TO_EMAIL:
        missing.append("TO_EMAIL")
    if not SMS_EMAIL:
        missing.append("SMS_EMAIL")

    if missing:
        raise RuntimeError("Missing required environment variables: " + ", ".join(missing))

    msg = MIMEText(body)
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = OUTLOOK_EMAIL
    msg["To"] = ", ".join([TO_EMAIL, SMS_EMAIL])

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)
        server.sendmail(
            OUTLOOK_EMAIL,
            [TO_EMAIL, SMS_EMAIL],
            msg.as_string()
        )


def main():
    print(f"Running Ulta reminder check for {TARGET_DATE}")
    today = datetime.now().strftime("%Y-%m-%d")

    if today == TARGET_DATE:
        body = "Reminder: Check Ulta Beauty today!"
    else:
        body = f"Test Run Successful — Today: {today}. Reminder is set for {TARGET_DATE}."

    send_email(body)


if __name__ == "__main__":
    main()
