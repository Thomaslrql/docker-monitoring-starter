import random, time
from fastapi import FastAPI, Response, status
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(version="v1.0.0")

# Ajoute instrumentation + expose /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/healthcheck")
def heathcheck():
    return {
        "status": "UP", 
        "version": app.version
    }

@app.get("/slow")
def slow():
    time.sleep(random.uniform(0.2, 1.2))
    return {"ok": True}

@app.get("/error")
def error(response: Response):
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"ok": False, "reason": "simulated error"}

@app.get("/live")
def live():
    return {"status": "ALIVE"}

@app.get("/ready")
def ready():
    return {"status": "READY"}
