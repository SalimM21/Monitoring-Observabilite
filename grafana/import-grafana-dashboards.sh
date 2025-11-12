#!/bin/bash

# Script pour importer les dashboards Grafana personnalisés
# Utilisation: ./import-grafana-dashboards.sh

set -e

# Configuration
GRAFANA_URL="http://localhost:3000"
GRAFANA_USER="admin"
GRAFANA_PASSWORD="admin"

# Fonction pour importer un dashboard
import_dashboard() {
    local dashboard_file=$1
    local dashboard_name=$(basename "$dashboard_file" .json)

    echo "Importation du dashboard: $dashboard_name"

    # Créer le payload pour l'API Grafana
    local payload=$(cat "$dashboard_file" | jq '.dashboard + {overwrite: true}')

    # Importer via API
    curl -s -X POST \
         -H "Content-Type: application/json" \
         -u "$GRAFANA_USER:$GRAFANA_PASSWORD" \
         -d "$payload" \
         "$GRAFANA_URL/api/dashboards/db" | jq -r '.status'

    echo "✅ Dashboard $dashboard_name importé"
}

# Vérifier que Grafana est accessible
echo "Vérification de la connexion à Grafana..."
if ! curl -s -u "$GRAFANA_USER:$GRAFANA_PASSWORD" "$GRAFANA_URL/api/health" > /dev/null; then
    echo "❌ Erreur: Grafana n'est pas accessible à $GRAFANA_URL"
    echo "   Vérifiez que le port-forwarding est actif:"
    echo "   kubectl port-forward svc/grafana-service 3000:3000 -n default"
    exit 1
fi

echo "✅ Grafana accessible"

# Importer les dashboards
echo "Importation des dashboards personnalisés..."

if [ -f "grafana-dashboards/scoring-ml-dashboard.json" ]; then
    import_dashboard "grafana-dashboards/scoring-ml-dashboard.json"
else
    echo "⚠️  Dashboard ML non trouvé: grafana-dashboards/scoring-ml-dashboard.json"
fi

if [ -f "grafana-dashboards/scoring-business-dashboard.json" ]; then
    import_dashboard "grafana-dashboards/scoring-business-dashboard.json"
else
    echo "⚠️  Dashboard Business non trouvé: grafana-dashboards/scoring-business-dashboard.json"
fi

echo ""
echo "🎉 Importation terminée!"
echo ""
echo "📊 Dashboards disponibles dans Grafana:"
echo "   - MLOps Scoring Platform - ML Metrics"
echo "   - MLOps Scoring Platform - Business Metrics"
echo ""
echo "🔗 Accès: http://localhost:3000 (admin/admin)"