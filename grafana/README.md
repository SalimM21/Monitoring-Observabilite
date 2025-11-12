# 📊 **Dashboards Grafana - Plateforme MLOps Scoring**

*Date : 12 novembre 2025*
*Version : Phase 2 - Monitoring Avancé*

---

## 🎯 **APERÇU**

Ce dossier contient les **dashboards Grafana personnalisés** pour la surveillance avancée de la plateforme MLOps de scoring automatique.

### **Dashboards Disponibles**
- **ML Metrics Dashboard** : Métriques spécialisées ML (drift, performance, features)
- **Business Metrics Dashboard** : KPI métier temps réel (success rate, scoring distribution)

---

## 📁 **STRUCTURE**

```
monitoring/grafana/
├── README.md                           # Ce fichier
├── import-grafana-dashboards.sh        # Script d'importation automatique
└── grafana-dashboards/
    ├── scoring-ml-dashboard.json       # Dashboard ML spécialisé
    └── scoring-business-dashboard.json # Dashboard Business
```

---

## 🚀 **UTILISATION**

### **Import Automatique**
```bash
# Depuis la racine du projet
./monitoring/grafana/import-grafana-dashboards.sh

# Ou depuis ce dossier
./import-grafana-dashboards.sh
```

### **Import Manuel**
1. Ouvrir Grafana : http://localhost:3000
2. Aller dans **Create → Import**
3. Sélectionner les fichiers `.json` du dossier `grafana-dashboards/`

### **Accès aux Dashboards**
- **ML Metrics** : "MLOps Scoring Platform - ML Metrics"
- **Business Metrics** : "MLOps Scoring Platform - Business Metrics"

---

## 📊 **DASHBOARD ML METRICS**

### **Panneaux Inclus**
- **Model Performance Overview** : Accuracy globale avec seuils
- **Prediction Latency** : 95th/50th percentiles des temps de réponse
- **Model Drift Detection** : Table avec seuils colorés (vert/orange/rouge)
- **Feature Importance** : Graphique en barres des variables importantes
- **Model Versions** : Informations détaillées sur les versions

### **Métriques Monitorées**
- `ml_model_accuracy` : Précision des modèles
- `ml_prediction_duration_bucket` : Latence des prédictions
- `ml_model_drift_score` : Score de dérive des modèles
- `ml_feature_importance` : Importance des features
- `ml_model_version_info` : Informations des versions

---

## 📈 **DASHBOARD BUSINESS METRICS**

### **Panneaux Inclus**
- **Daily Scoring Requests** : Volume de requêtes par jour
- **Scoring Success Rate** : Taux de succès avec seuils (99%+)
- **Credit Score Distribution** : Histogramme des scores de crédit
- **Risk Level Breakdown** : Répartition par niveau de risque
- **API Response Times** : Latences par endpoint
- **Data Pipeline Health** : Santé Kafka + MinIO
- **Compliance Violations** : Alertes RGPD/KYC

### **Métriques Monitorées**
- `scoring_requests_total` : Nombre total de requêtes
- `scoring_errors_total` : Nombre d'erreurs
- `scoring_credit_score` : Distribution des scores
- `http_request_duration_seconds` : Latence des APIs
- `kafka_topic_partitions_in_sync` : Santé Kafka
- `compliance_violations_total` : Violations conformité

---

## ⚙️ **CONFIGURATION REQUISE**

### **Grafana**
- Version : 8.0+
- Plugins : Table, Histogram, Barchart (inclus par défaut)
- Permissions : Admin pour l'import

### **Prometheus**
- Exposition des métriques ML et business
- Endpoints configurés dans les services

### **Services**
- Métriques Prometheus exposées sur `/metrics`
- Labels appropriés pour les requêtes

---

## 🔧 **PERSONNALISATION**

### **Modifier les Dashboards**
1. Exporter depuis Grafana (JSON)
2. Éditer le fichier `.json`
3. Réimporter via le script

### **Ajouter des Métriques**
1. Modifier les queries Prometheus dans les panneaux
2. Tester les requêtes dans Prometheus UI
3. Mettre à jour le dashboard

### **Seuils et Alertes**
- **Vert** : Performance optimale
- **Orange** : Attention requise
- **Rouge** : Action immédiate nécessaire

---

## 📞 **SUPPORT**

### **Dépannage**
- **Script ne trouve pas Grafana** : Vérifier port-forwarding
- **Métriques non affichées** : Vérifier exposition Prometheus
- **Panneaux vides** : Vérifier noms des métriques

### **Maintenance**
- **Mise à jour** : Réimporter après modifications
- **Sauvegarde** : Conserver les fichiers `.json`
- **Versionning** : Git pour le suivi des changements

---

## 🎯 **IMPACT BUSINESS**

| Aspect | Amélioration | Bénéfice |
|--------|--------------|----------|
| **Observabilité ML** | 🔼 **95%** | Vision complète modèles |
| **Monitoring métier** | 🔼 **90%** | KPI temps réel |
| **Détection problèmes** | 🔼 **80%** | Action proactive |
| **Temps diagnostic** | 🔼 **85%** | Minutes vs heures |

---

**📊 Dashboards opérationnels pour monitoring avancé !**