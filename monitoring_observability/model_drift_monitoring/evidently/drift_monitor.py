from prometheus_client import start_http_server, Gauge
import pandas as pd
from evidently import ColumnMapping
from evidently.metrics import DatasetDriftMetric
from evidently.report import Report
import time
import json

# -----------------------------
# Définir les métriques Prometheus
# -----------------------------
MODEL_DRIFT = Gauge('model_drift_score', 'Score de dérive du modèle ML')

# -----------------------------
# Fichiers CSV ou JSON des données
# -----------------------------
TRAIN_DATA_PATH = "train_data.csv"
PROD_DATA_PATH = "prod_data.csv"

# -----------------------------
# Fonction de calcul de dérive
# -----------------------------
def calculate_drift(train_path, prod_path):
    train_df = pd.read_csv(train_path)
    prod_df = pd.read_csv(prod_path)

    # Mapping des colonnes si besoin
    column_mapping = ColumnMapping()

    # Créer le rapport Evidently
    report = Report(metrics=[DatasetDriftMetric()])
    report.run(reference_data=train_df, current_data=prod_df, column_mapping=column_mapping)

    # Extraire le score de dérive global
    drift_score = report.metrics[0]['result']['dataset_drift']
    return drift_score

# -----------------------------
# Boucle principale
# -----------------------------
if __name__ == "__main__":
    start_http_server(9102)  # Exposer métriques sur Prometheus

    while True:
        try:
            score = calculate_drift(TRAIN_DATA_PATH, PROD_DATA_PATH)
            MODEL_DRIFT.set(score)
            print(f"Drift Score: {score}")
        except Exception as e:
            print(f"Erreur lors du calcul de dérive: {e}")
            MODEL_DRIFT.set(0)

        time.sleep(600)  # Rafraîchissement toutes les 10 minutes
