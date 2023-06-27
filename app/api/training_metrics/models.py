from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field
from uuid import uuid4


class TrainingPlanMetricType(str, Enum):
    score = "score"
    usage = "usage"


class TrainingPlanMetrics(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    training_id: str
    favourite_counter: int = Field(default=0)
    review_counter: int = Field(default=0)
    completed_counter: int = Field(default=0)
    fulfilled_counter: int = Field(default=0)
    review_average: float = Field(default=0.0)


class ScoreMetric(BaseModel):
    metric_type: Literal[TrainingPlanMetricType.score]
    favourite_counter: int
    review_counter: int
    review_average: float


class UsageMetric(BaseModel):
    metric_type: Literal[TrainingPlanMetricType.usage]
    completed_counter: int
    fulfilled_counter: int


class TrainingPlanMetricsRequest(BaseModel):
    metric: ScoreMetric | UsageMetric = Field(..., discriminator="metric_type")
