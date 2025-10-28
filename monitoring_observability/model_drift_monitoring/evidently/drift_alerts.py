import time
import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import logging
import requests
import os

# -----------------------------
# Configuration
# -----------------------------
TRAIN_DATA_PATH = "train_data.csv"
PROD_DATA_PATH = "prod_data.csv"
DRIFT_THRESHOLD = 0.1  # seuil critique
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "http://pushgateway:9091")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# -----------------------------
# Logger
# -----------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------
# Fonction calcul dérive
# -----------------------------
def calculate_drift(train_path, prod_path):
    train_df = pd.read_csv(train_path)
    prod_df = pd.read_csv(prod_path)
    column_mapping = ColumnMapping()
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(reference_data=train_df, current_data=prod_df, column_mapping=column_mapping)
    return report.metrics[0]['result']['dataset_drift']

# -----------------------------
# Fonction alerte Slack
# -----------------------------
def send_slack_alert(message):
    if SLACK_WEBHOOK_URL:
        payload = {"text": message}
        try:
            requests.post(SLACK_WEBHOOK_URL, json=payload)
        except Exception as e:
            logging.error(f"Erreur Slack: {e}")

# -----------------------------
# Fonction PushGateway
# -----------------------------
def push_to_prometheus(drift_score):
    try:
        registry = CollectorRegistry()
        g = Gauge('model_drift_score', 'Score de dérive du modèle ML', registry=registry)
        g.set(drift_score)
        push_to_gateway(PUSHGATEWAY_URL, job='model_drift_monitor', registry=registry)
    except Exception as e:
        logging.error(f"Erreur PushGateway: {e}")

# -----------------------------
# Boucle principale
# -----------------------------
if __name__ == "__main__":
    while True:
        try:
            score = calculate_drift(TRAIN_DATA_PATH, PROD_DATA_PATH)
            logging.info(f"Score de dérive: {score}")

            # Pousser métrique à Prometheus
            push_to_prometheus(score)

            # Vérifier seuil et envoyer alerte si nécessaire
            if score > DRIFT_THRESHOLD:
                message = f"⚠️ Alerte dérive modèle : Score = {score} (> {DRIFT_THRESHOLD})"
                logging.warning(message)
                send_slack_alert(message)

        except Exception as e:
            logging.error(f"Erreur lors du calcul/alerte de dérive: {e}")

        time.sleep(600)  # vérifier toutes les 10 minutes
