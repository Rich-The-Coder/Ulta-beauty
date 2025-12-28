from datetime import date
import smtplib
from email.mime.text import MIMEText
import os

OUTLOOK_EMAIL = os.getenv("OUTLOOK_EMAIL")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
SMS_EMAIL = os.getenv("SMS_EMAIL")

REMINDER_MESSAGES = {
    date(2026, 1, 14): "One week until Ulta Beauty World 2026 tickets (Jan 21). Check Ulta today.",
    date(2026, 1, 21): "TODAY is the expected Ulta Beauty World ticket drop. GO!",
    date(2026, 2, 19): "Backup reminder: 1 week until possible Feb 26 Ulta ticket sale.",
    date(2026, 2, 26): "Backup sale date TODAY. Check Ulta tickets now!"
}

EMAIL_SUBJECT = "Ulta Beauty World 2026 Reminder"


def send_email(body: str):
    msg = MIMEText(body)
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = OUTLOOK_EMAIL
    msg["To"] = ", ".join([TO_EMAIL, SMS_EMAIL])

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
        server.starttls()
        server.login(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)
        server.sendmail(
            OUTLOOK_EMAIL,
            [TO_EMAIL, SMS_EMAIL],
            msg.as_string()
        )


def main():
    today = date.today()
    print(f"Running Ulta reminder check for {today}")

    if today in REMINDER_MESSAGES:
        body = REMINDER_MESSAGES[today] + "\n\nUlta Beauty World 2026 – Orlando"
        send_email(body)
        print("Reminder sent.")
    else:
        print("No reminder today.")


if __name__ == "__main__":
    main()
