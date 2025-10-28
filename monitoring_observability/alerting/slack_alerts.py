import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# -----------------------------
# Configuration
# -----------------------------
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
EMAIL_ALERT = os.getenv("EMAIL_ALERT", "false").lower() == "true"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER", "alert@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "password")
EMAIL_TO = os.getenv("EMAIL_TO", "team@example.com")

# Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------
# Fonction envoi Slack
# -----------------------------
def send_slack_alert(message: str):
    if not SLACK_WEBHOOK_URL:
        logging.warning("SLACK_WEBHOOK_URL non configuré")
        return
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            logging.error(f"Erreur Slack: {response.status_code} - {response.text}")
        else:
            logging.info("Alerte Slack envoyée")
    except Exception as e:
        logging.error(f"Exception Slack: {e}")

# -----------------------------
# Fonction envoi Email
# -----------------------------
def send_email_alert(subject: str, body: str):
    if not EMAIL_ALERT:
        return
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.quit()
        logging.info("Alerte email envoyée")
    except Exception as e:
        logging.error(f"Erreur envoi email: {e}")

# -----------------------------
# Exemple d'utilisation
# -----------------------------
if __name__ == "__main__":
    test_message = "⚠️ Alerte dérive modèle : Score > seuil critique"
    send_slack_alert(test_message)
    send_email_alert("Alerte dérive modèle", test_message)
