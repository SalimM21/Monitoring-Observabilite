# Monitoring-Observabilite
la partie Monitoring &amp; Observabilité (User Stories 7.1 &amp; 7.2) du projet de plateforme de scoring/prediction ML. Cette structure combine la surveillance des performances API (Prometheus + Grafana) et la détection de dérive des modèles (EvidentlyAI).

## Description 
Ce module implémente la surveillance des performances des APIs et des modèles ML dans la plateforme de scoring/fraude. Il couvre trois aspects principaux : 
1.**Monitoring des APIs (User Story 7.1)** 
    - Collecte des métriques temps de réponse, taux d’erreur et SLA.
    - Visualisation via Grafana.
    - Alertes automatiques si SLA dépassé (> 2s).
2. **Détection dela dérive des modèles ML (User Story 7.2)**
    - Surveillance des distributions des features entre les données d’entraînement et la production.
    - Génération de rapports HTML/JSON via EvidentlyAI.
    - Alerte automatique en cas de dérive significative (`drift_score > seuil`).
3. **Centralisation des logs et traces (User Story 7.3)**
    - Collecte centralisée des logs des APIs et modèles.
    - Visualisation via Kibana et suivi des traces avec Jaeger/OpenTelemetry.
    - Alertes sur erreurs critiques.
## Arborescence


