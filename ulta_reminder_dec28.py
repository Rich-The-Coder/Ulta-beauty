from datetime import date
import smtplib
from email.mime_text import MIMEText
import os

"""
Ulta Beauty World reminder script

This script is meant to be run once per day (for example by GitHub Actions).
It checks today's date; if it matches one of the REMINDER_MESSAGES keys,
it sends an email + SMS (via email gateway).
"""

# These should be set as environment variables (for GitHub Actions, use Secrets)
OUTLOOK_EMAIL = os.getenv("OUTLOOK_EMAIL")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
SMS_EMAIL = os.getenv("SMS_EMAIL")

# Dates to send reminders on
REMINDER_MESSAGES = {
    # Custom reminder for December 28, 2025
    date(2025, 12, 28): "Ulta Beauty reminder — it is December 28. Check Ulta and make sure you are ready for ticket drops!",

    # 2026 Ulta World ticket-related reminders
    date(2026, 1, 14): "One week until Ulta Beauty World 2026 tickets (Jan 21). Check Ulta today and watch for announcements.",
    date(2026, 1, 21): "TODAY is the expected Ulta Beauty World 2026 ticket drop (Jan 21). Go check tickets now!",
    date(2026, 2, 19): "Backup reminder: 1 week until possible Feb 26 Ulta ticket sale. Double-check Ulta's site and socials.",
    date(2026, 2, 26): "Backup sale date is TODAY (Feb 26). Check Ulta tickets now so you don't miss out."
}

EMAIL_SUBJECT = "Ulta Beauty World Reminder"


def send_email(body: str) -> None:
    """
    Send a message to both TO_EMAIL and SMS_EMAIL using Outlook SMTP.
    """
    if not OUTLOOK_EMAIL or not OUTLOOK_PASSWORD or not TO_EMAIL or not SMS_EMAIL:
        raise RuntimeError("Missing one or more required environment variables: "
                           "OUTLOOK_EMAIL, OUTLOOK_PASSWORD, TO_EMAIL, SMS_EMAIL")

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


def main() -> None:
    today = date.today()
    print(f"Running Ulta reminder check for {today}")

    if today in REMINDER_MESSAGES:
        body = REMINDER_MESSAGES[today] + "\n\nUlta Beauty World – don't miss it."
        send_email(body)
        print("Reminder sent.")
    else:
        print("No reminder scheduled for today.")


if __name__ == "__main__":
    main()
