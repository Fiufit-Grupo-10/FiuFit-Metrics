from fastapi import APIRouter, HTTPException, Request, status
from .models import TrainingPlanMetrics, TrainingPlanMetricsRequest
from . import crud
from fastapi.responses import JSONResponse


router = APIRouter(tags=["training_metrics"])


@router.put("/metrics/trainings/{training_id}")
async def update_metric(
    training_id: str, metrics: TrainingPlanMetricsRequest, request: Request
):
    result = await crud.update_metric(
        training_id=training_id, metrics=metrics, request=request
    )
    return JSONResponse(status_code=result[1], content=result[0])


@router.get("/metrics/trainings/{training_id}", response_model=TrainingPlanMetrics)
async def get_metrics(training_id: str, request: Request):
    result = await crud.get_metrics(training_id=training_id, request=request)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"training with id:{training_id} not found",
        )
    return result
