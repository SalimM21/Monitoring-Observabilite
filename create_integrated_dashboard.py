#!/usr/bin/env python3
"""
Script pour créer un dashboard intégré combinant les métriques
de tous les modules : Monitoring, Audit, et Data Pipelines
"""

import json
import requests
from datetime import datetime

def create_integrated_dashboard():
    """Crée un dashboard Grafana intégré"""

    dashboard = {
        "dashboard": {
            "title": "Plateforme Scoring - Dashboard Intégré",
            "tags": ["scoring", "mlops", "integrated"],
            "timezone": "UTC",
            "panels": [
                # Panel 1: Métriques API
                {
                    "title": "Performance API Scoring",
                    "type": "graph",
                    "targets": [{
                        "expr": "rate(http_requests_total[5m])",
                        "legendFormat": "Requêtes/minute"
                    }]
                },
                # Panel 2: Qualité des données
                {
                    "title": "Score Qualité Données",
                    "type": "singlestat",
                    "targets": [{
                        "expr": "data_quality_score",
                        "legendFormat": "Qualité"
                    }]
                },
                # Panel 3: Dérive du modèle
                {
                    "title": "Dérive du Modèle ML",
                    "type": "graph",
                    "targets": [{
                        "expr": "model_drift_score",
                        "legendFormat": "Score de dérive"
                    }]
                },
                # Panel 4: Violations de conformité
                {
                    "title": "Alertes Conformité",
                    "type": "table",
                    "targets": [{
                        "expr": "compliance_violations_total",
                        "legendFormat": "Violations"
                    }]
                }
            ],
            "time": {
                "from": "now-1h",
                "to": "now"
            },
            "refresh": "30s"
        }
    }

    # Sauvegarder le dashboard
    with open('integrated_dashboard.json', 'w') as f:
        json.dump(dashboard, f, indent=2)

    print("Dashboard intégré créé : integrated_dashboard.json")

if __name__ == "__main__":
    create_integrated_dashboard()
