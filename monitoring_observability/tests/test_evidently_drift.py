import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric

TRAIN_DATA_PATH = "train_data.csv"
PROD_DATA_PATH = "prod_data.csv"

def test_drift_monitor():
    try:
        # Charger les données
        train_df = pd.read_csv(TRAIN_DATA_PATH)
        prod_df = pd.read_csv(PROD_DATA_PATH)

        # Mapping des colonnes (optionnel)
        column_mapping = ColumnMapping()

        # Créer rapport Evidently
        report = Report(metrics=[DatasetDriftMetric()])
        report.run(reference_data=train_df, current_data=prod_df, column_mapping=column_mapping)

        # Récupérer score de dérive global
        drift_score = report.metrics[0]['result']['dataset_drift']
        print(f"✅ Drift monitor fonctionne, score global de dérive : {drift_score:.4f}")

        # Vérification simple
        assert 0 <= drift_score <= 1, "Score de dérive invalide !"
        return True

    except Exception as e:
        print(f"❌ Erreur drift monitor : {e}")
        return False

if __name__ == "__main__":
    if not test_drift_monitor():
        exit(1)
