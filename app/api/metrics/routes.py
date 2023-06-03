from fastapi import APIRouter, HTTPException, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
from app.config.database import METRICS_COLLECTION_NAME


from app.api.metrics.models import (
    UserMetric,
)


router = APIRouter(tags=["metrics"])


@router.post("/metrics", response_model=UserMetric)
async def create_metric(metric: UserMetric, request: Request):
    metric = jsonable_encoder(metric)
    new_metric = await request.app.mongodb[METRICS_COLLECTION_NAME].insert_one(metric)
    created_metric = await request.app.mongodb[METRICS_COLLECTION_NAME].find_one(
        {"_id": new_metric.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_metric)
