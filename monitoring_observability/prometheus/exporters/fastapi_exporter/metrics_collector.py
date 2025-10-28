from prometheus_client import start_http_server, Summary, Counter, Gauge
from fastapi import FastAPI, Request
import random
import time
import uvicorn

# -----------------------------
# Définition des métriques Prometheus
# -----------------------------
REQUEST_TIME = Summary('request_processing_seconds', 'Temps de traitement des requêtes')
ERRORS = Counter('api_errors_total', 'Nombre total d\'erreurs API')
REQUEST_COUNT = Counter('api_requests_total', 'Nombre total de requêtes API')
LAST_REQUEST_LATENCY = Gauge('last_request_latency_seconds', 'Latence de la dernière requête')

# -----------------------------
# Application FastAPI simulée
# -----------------------------
app = FastAPI()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    LAST_REQUEST_LATENCY.set(latency)
    REQUEST_TIME.observe(latency)
    REQUEST_COUNT.inc()

    # Simuler erreurs aléatoires (5% de probabilité)
    if random.random() < 0.05:
        ERRORS.inc()
        response.status_code = 500

    return response

@app.get("/hello")
async def hello():
    return {"message": "Hello from API Exporter!"}

# -----------------------------
# Lancer le serveur Prometheus metrics
# -----------------------------
if __name__ == "__main__":
    # Expose les métriques sur le port 8001
    start_http_server(8001)
    # Lancer l'API FastAPI sur le même port pour la simulation
    uvicorn.run(app, host="0.0.0.0", port=8001)
