from fastapi import Request
from app.api.training_metrics.models import (
    TrainingPlanMetricsRequest,
    TrainingPlanMetrics,
)
from app.config.database import TRAINING_METRICS_COLLECTION_NAME
from fastapi.encoders import jsonable_encoder


async def update_metric(
    training_id: str, metrics: TrainingPlanMetricsRequest, request: Request
):
    old_metrics = await request.app.mongodb[TRAINING_METRICS_COLLECTION_NAME].find_one(
        {"training_id": training_id}
    )
    response_code = 200
    if old_metrics is None:
        old_metrics = TrainingPlanMetrics(training_id=training_id)
        old_metrics = jsonable_encoder(old_metrics)
        response_code = 201
    else:
        await request.app.mongodb[TRAINING_METRICS_COLLECTION_NAME].delete_one(
            {"training_id": training_id}
        )

    if metrics.metric.metric_type == "score":
        old_metrics["favourite_counter"] = metrics.metric.favourite_counter
        old_metrics["review_counter"] = metrics.metric.review_counter
        old_metrics["review_average"] = metrics.metric.review_average
    else:
        old_metrics["completed_counter"] = metrics.metric.completed_counter
        old_metrics["fulfilled_counter"] = metrics.metric.fulfilled_counter

    await request.app.mongodb[TRAINING_METRICS_COLLECTION_NAME].insert_one(old_metrics)
    updated_metrics = await request.app.mongodb[
        TRAINING_METRICS_COLLECTION_NAME
    ].find_one({"training_id": training_id})
    return (updated_metrics, response_code)


async def get_metrics(training_id: str, request: Request):
    return await request.app.mongodb[TRAINING_METRICS_COLLECTION_NAME].find_one(
        {"training_id": training_id}
    )
