import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_alert_email(recipient_email: str, metric_name: str, insights_text: str) -> bool:
    sender = os.getenv("ALERT_EMAIL_SENDER")
    password = os.getenv("ALERT_EMAIL_PASSWORD")

    if not sender or not password:
        return False

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient_email
    msg["Subject"] = f"🚨 Anomaly Alert: Unusual activity detected in {metric_name}"

    body = f"""Hello,

Our automated data monitor detected unusual numbers in your latest report for: {metric_name}.

Here is the quick diagnosis:

{insights_text}

---
Generated automatically by your AI Data Monitor.
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False