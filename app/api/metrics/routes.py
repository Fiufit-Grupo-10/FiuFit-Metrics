from datetime import datetime
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


@router.get("/metrics")
async def get_metrics(
    request: Request,
    metric_type: str,
    start_date: str = Query(..., description="Start date in ISO format"),
    end_date: str = Query(..., description="End date in ISO format"),
):
    results = (
        await request.app.mongodb[METRICS_COLLECTION_NAME]
        .find(
            {
                "metric.metric_type": metric_type,
                "updated": {"$lte": end_date, "$gte": start_date},
            }
        )
        .to_list(None)
    )
    return results
