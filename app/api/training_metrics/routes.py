from fastapi import APIRouter, HTTPException, Request, status
from app.api.goals import service
from app.api.goals.models import Goal, UserGoalsReturn

router = APIRouter(tags=["training_metrics"])

# Identificamos por el id del entrenamiento
# TRAININGS | GOALS

@router.put("/metrics/trainings/{id}")
def update_metric():
    pass

@router.get("/metrics/trainings/{id}")
def get_metrics():
    pass
