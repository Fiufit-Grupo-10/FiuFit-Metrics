from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
from app.config.database import METRICS_COLLECTION_NAME


from app.api.metrics.models import (
    TotalGeographicalResponse,
    UserByDepartment,
    UserByProvince,
    UserMetric,
    TotalMetricsResponse,
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
    start_date: str
    | None = Query(default=None, description="Start date in ISO format"),
    end_date: str | None = Query(default=None, description="End date in ISO format"),
):
    query = {"metric.metric_type": metric_type}
    if start_date is not None and end_date is not None:
        query["updated"] = {"$lte": end_date, "$gte": start_date}

    results = (
        await request.app.mongodb[METRICS_COLLECTION_NAME].find(query).to_list(None)
    )
    return results


@router.get("/metrics/totals", response_model=TotalMetricsResponse)
async def get_totals(
    request: Request,
):
    pipeline = [{"$group": {"_id": "$metric.metric_type", "count": {"$sum": 1}}}]

    result = request.app.mongodb[METRICS_COLLECTION_NAME].aggregate(pipeline)

    data = {}

    async for doc in result:
        data[doc["_id"]] = doc["count"]

    total_metrics_response = TotalMetricsResponse(**data)

    return total_metrics_response


@router.get("/metrics/locations", response_model=TotalGeographicalResponse)
async def get_geo_stats(request: Request, register_type: str):
    province_pipeline = [
        {"$match": {"metric.metric_type": register_type}},
        {"$group": {"_id": "$metric.geographic_zone.province", "count": {"$sum": 1}}},
    ]

    department_pipeline = [
        {"$match": {"metric.metric_type": register_type}},
        {"$group": {"_id": "$metric.geographic_zone.department", "count": {"$sum": 1}}},
    ]

    province_result = request.app.mongodb[METRICS_COLLECTION_NAME].aggregate(
        province_pipeline
    )
    deparment_result = request.app.mongodb[METRICS_COLLECTION_NAME].aggregate(
        department_pipeline
    )

    departments = []
    async for result in deparment_result:
        departments.append(
            UserByDepartment(department=result["_id"], counter=result["count"])
        )

    provinces = []
    async for result in province_result:
        provinces.append(
            UserByProvince(province=result["_id"], counter=result["count"])
        )

    return TotalGeographicalResponse(provinces=provinces, departments=departments)
