from fastapi import APIRouter, Response
from prometheus_client import generate_latest

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])


@base_router.get("/")
async def welcome():
    return {"status": "Health Check"}


@base_router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
