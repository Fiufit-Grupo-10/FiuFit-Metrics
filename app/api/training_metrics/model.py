from pydantic import BaseModel

class TrainingPlanMetrics(BaseModel):
    plan_id: str
    favourite_counter: int
    review_counter: int
    completed_counter: int
    fulfilled_counter: int
    review_average: float


class A(BaseModel):
    favourite_counter: int
    review_counter: int
    review_average: float


class B(BaseModel):
    completed_counter: int
    fulfilled_counter: int


RequestBody = A | B
