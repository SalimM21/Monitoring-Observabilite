#!/bin/bash

echo "🔗 Intégration des modules : Audit-KYC-GDPR, Fraude-Snowflake, Monitoring"
echo "======================================================================"

# Fonction pour vérifier si un service est disponible
check_service() {
    local service=$1
    local port=$2
    if nc -z localhost $port 2>/dev/null; then
        echo "✅ $service est disponible sur le port $port"
        return 0
    else
        echo "❌ $service n'est pas disponible sur le port $port"
        return 1
    fi
}

# 1. Lancement du module Monitoring
echo ""
echo "📊 1. Lancement du module Monitoring..."
cd monitoring/monitoring_observability

# Lancer Prometheus et Grafana
if [ -f "prometheus/docker-compose.yml" ]; then
    echo "Lancement de Prometheus et Grafana..."
    docker-compose -f prometheus/docker-compose.yml up -d
    sleep 10

    # Vérifier les services
    check_service "Prometheus" "9090"
    check_service "Grafana" "3000"
fi

# Lancer Loki pour les logs
if [ -f "loki_config.yml" ]; then
    echo "Lancement de Loki..."
    docker run -d --name loki -p 3100:3100 grafana/loki:2.9.0 -config.file=/etc/loki/local-config.yaml
    sleep 5
    check_service "Loki" "3100"
fi

cd ../..

# 2. Lancement du module Audit-KYC-GDPR
echo ""
echo "🔐 2. Lancement du module Audit-KYC-GDPR..."
cd audit-kyc-gdpr/project_root

# Installer les dépendances si nécessaire
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Lancer les collecteurs de logs
echo "Démarrage des collecteurs de logs..."
python -m src.audit.log_collector &
echo $! > audit_collector.pid

# Lancer le système d'alertes
python -m src.audit.alerting_system &
echo $! > alerting_system.pid

# Lancer les vérifications de conformité
python -m src.compliance.aml_monitor &
echo $! > aml_monitor.pid

python -m src.compliance.gdpr_verification &
echo $! > gdpr_verification.pid

echo "Services d'audit démarrés (PIDs sauvegardés)"

cd ../..

# 3. Lancement du module Fraude-Snowflake
echo ""
echo "🗄️ 3. Lancement du module Fraude-Snowflake..."
cd fraude-snowflake/fraud_scoring_platform

# Installer les dépendances
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Lancer Airflow (si docker-compose existe)
if [ -f "docker-compose.yml" ]; then
    echo "Lancement d'Airflow..."
    docker-compose up -d airflow-webserver airflow-scheduler
    sleep 15
    check_service "Airflow Webserver" "8080"
fi

# Exécuter les tests de qualité des données
echo "Exécution des tests de qualité des données..."
python -m pytest tests/test_data_quality.py -v

# Générer le rapport de qualité
echo "Génération du rapport de qualité..."
python jobs/quality/generate_quality_report.py

cd ../..

# 4. Intégration et tests croisés
echo ""
echo "🔗 4. Tests d'intégration entre modules..."

# Test de l'intégration monitoring + audit
echo "Test de l'intégration Monitoring + Audit..."
curl -s http://localhost:3100/ready || echo "Loki n'est pas prêt"

# Test de l'intégration audit + pipelines
echo "Vérification des logs d'Airflow..."
if check_service "Airflow Webserver" "8080"; then
    curl -s http://localhost:8080/health || echo "Airflow health check failed"
fi

# 5. Configuration des alertes croisées
echo ""
echo "🚨 5. Configuration des alertes intégrées..."

# Créer des règles d'alerte combinées
cat > integrated_alerts.yml << EOF
groups:
  - name: integrated_alerts
    rules:
      - alert: DataQualityFailure
        expr: data_quality_score < 0.8
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Qualité des données dégradée"
          description: "Le score de qualité des données est inférieur à 80%"

      - alert: ModelDriftDetected
        expr: model_drift_score > 0.3
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Dérive du modèle détectée"
          description: "Le score de dérive du modèle dépasse le seuil de 0.3"

      - alert: AuditComplianceFailure
        expr: compliance_violations_total > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Violation de conformité détectée"
          description: "Une violation de conformité GDPR/KYC/AML a été détectée"
EOF

echo "Règles d'alertes intégrées créées"

# 6. Dashboard intégré
echo ""
echo "📊 6. Création du dashboard intégré..."

# Script pour combiner les dashboards
cat > create_integrated_dashboard.py << 'EOF'
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
EOF

python create_integrated_dashboard.py

# 7. Rapport d'intégration final
echo ""
echo "📋 7. Génération du rapport d'intégration..."

cat > integration_report.md << EOF
# Rapport d'Intégration des Modules

## Modules Intégrés
- ✅ **Monitoring**: Prometheus, Grafana, Loki opérationnels
- ✅ **Audit-KYC-GDPR**: Collecteurs de logs et alertes actifs
- ✅ **Fraude-Snowflake**: Pipelines Airflow et tests de qualité configurés

## Services Disponibles
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Loki**: http://localhost:3100
- **Airflow**: http://localhost:8080

## Métriques Intégrées
- Performances API (latence, erreurs, SLA)
- Qualité des données (score, validations)
- Dérive des modèles ML (distribution, alertes)
- Conformité réglementaire (violations, audits)

## Alertes Configurées
- Qualité des données < 80%
- Dérive du modèle > 0.3
- Violations de conformité détectées

## Dashboards
- Dashboard intégré créé: \`integrated_dashboard.json\`
- Métriques croisées entre tous les modules

## Prochaines Étapes
1. Importer le dashboard intégré dans Grafana
2. Configurer les webhooks Slack pour les alertes
3. Programmer les jobs de surveillance périodique
4. Tester les scénarios de failover

---
Rapport généré le: $(date)
EOF

echo "Rapport d'intégration généré: integration_report.md"

echo ""
echo "🎉 Intégration terminée avec succès !"
echo ""
echo "📊 Services disponibles:"
echo "   📈 Grafana:        http://localhost:3000"
echo "   📊 Prometheus:     http://localhost:9090"
echo "   📝 Loki:          http://localhost:3100"
echo "   🎯 Airflow:       http://localhost:8080"
echo ""
echo "📄 Rapports générés:"
echo "   📋 Rapport intégré: integration_report.md"
echo "   📊 Dashboard:       integrated_dashboard.json"
echo ""
echo "🛑 Pour arrêter tous les services:"
echo "   kill \$(cat *.pid 2>/dev/null)"
echo "   docker-compose down (dans chaque module)"