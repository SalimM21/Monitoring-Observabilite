import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric, DataQualityMetric, ClassificationPerformanceMetric

# -----------------------------
# Fichiers de données
# -----------------------------
TRAIN_DATA_PATH = "train_data.csv"
PROD_DATA_PATH = "prod_data.csv"

# -----------------------------
# Charger les données
# -----------------------------
train_df = pd.read_csv(TRAIN_DATA_PATH)
prod_df = pd.read_csv(PROD_DATA_PATH)

# -----------------------------
# Mapping des colonnes (si nécessaire)
# -----------------------------
column_mapping = ColumnMapping()

# -----------------------------
# Créer le rapport Evidently
# -----------------------------
report = Report(metrics=[
    DatasetDriftMetric(),
    DataQualityMetric(),
    ClassificationPerformanceMetric()
])

# Exécuter le rapport
report.run(reference_data=train_df, current_data=prod_df, column_mapping=column_mapping)

# -----------------------------
# Exporter le rapport en HTML
# -----------------------------
report.save_html("model_monitoring_report.html")
print("Rapport Evidently généré : model_monitoring_report.html")
