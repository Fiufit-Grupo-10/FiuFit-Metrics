from fastapi import FastAPI
from app.api.metrics import routes as metrics_routes
from app.api.training_metrics import routes as training_metrics_routes
from app.config.database import DB_NAME, MONGO_METRICS_URL
from app.config.config import DEV_ENV
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from ddtrace.contrib.asgi import TraceMiddleware
from ddtrace import config

# Override service name
config.fastapi['service_name'] = 'metrics-service'

app = FastAPI()
if DEV_ENV == "true":
    app.add_middleware(TraceMiddleware)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_METRICS_URL)
    app.mongodb_client.get_io_loop = asyncio.get_event_loop
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(metrics_routes.router)
app.include_router(training_metrics_routes.router)
