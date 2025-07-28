from fastapi import APIRouter, Response
from prometheus_client import Counter, generate_latest

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])
REQUEST_COUNT = Counter("app_requests_total", "Total HTTP requests")


@base_router.get("/")
async def welcome():
    REQUEST_COUNT.inc()
    return {"status": "Health Check"}

@base_router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")