import os

# Définition de la structure du projet Monitoring & Observabilité
project_structure = {
    "prometheus": {
        "prometheus.yml": None,
        "alert_rules.yml": None,
        "docker-compose.yml": None,
        "exporters": {
            "node_exporter": ["dockerfile"],
            "fastapi_exporter": ["metrics_collector.py", "requirements.txt"],
            "kafka_exporter": ["dockerfile"]
        }
    },

    "grafana": {
        "dashboards": [
            "api_performance.json",
            "system_metrics.json",
            "model_drift.json"
        ],
        "datasources": ["prometheus.yml"],
        "provisioning": ["dashboards.yaml", "datasources.yaml"]
    },

    "model_drift_monitoring": {
        "evidently": [
            "drift_monitor.py",
            "report_generator.py",
            "drift_alerts.py",
            "config_drift.yaml"
        ],
        "reports": {
            "drift_report_latest.html": None,
            "drift_history": [
                "2025-10-10_drift.html",
                "2025-10-11_drift.html"
            ]
        },
        "notebooks": ["explore_drift.ipynb"]
    },

    "alerting": {
        "slack_alerts.py": None,
        "alertmanager.yml": None,
        "templates": ["alert_template.tmpl"]
    },

    "tests": [
        "test_prometheus_config.py",
        "test_grafana_dashboards.py",
        "test_evidently_drift.py",
        "test_alerts.py"
    ],

    "README.md": None
}


def create_structure(base_path, structure):
    """Crée récursivement les dossiers et fichiers du projet"""
    for name, content in structure.items() if isinstance(structure, dict) else []:
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            print(f"[📁 Dossier] {path}")
            create_structure(path, content)

        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            print(f"[📁 Dossier] {path}")
            for file in content:
                file_path = os.path.join(path, file)
                open(file_path, "a").close()
                print(f"   [📄 Fichier] {file_path}")

        elif content is None:
            open(path, "a").close()
            print(f"[📄 Fichier] {path}")


if __name__ == "__main__":
    root_dir = "monitoring_observability"
    os.makedirs(root_dir, exist_ok=True)
    print(f"🚀 Création de la structure du projet dans : {os.path.abspath(root_dir)}\n")
    create_structure(root_dir, project_structure)
    print("\n✅ Arborescence 'monitoring_observability' créée avec succès !")
