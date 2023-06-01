from enum import Enum
from typing import Tuple
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Literal


class MetricType(str, Enum):
    register_with_email_and_password = "register_with_email_and_password"
    register_with_federeted_identity = "register_with_federated_identity"
    login_with_email_and_password = "login_with_email_and_password"
    login_with_federeted_identity = "login_with_federeted_identity"
    blocked_user = "blocked_user"
    password_recover = "password_recover"


class NewUser(BaseModel):
    metric_type: Literal[
        MetricType.register_with_email_and_password,
        MetricType.register_with_federeted_identity,
    ]
    latitude: float
    longitude: float


class Login(BaseModel):
    metric_type: Literal[
        MetricType.login_with_federeted_identity,
        MetricType.login_with_email_and_password,
    ]


class BlockedUser(BaseModel):
    metric_type: Literal[MetricType.blocked_user]


class PasswordRecover(BaseModel):
    metric_type: Literal[MetricType.password_recover]


class UserMetric(BaseModel):
    metric: NewUser | Login | BlockedUser | PasswordRecover = Field(
        ..., discriminator="metric_type"
    )
    id: str = Field(default_factory=uuid4, alias="_id")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "metric": {
                    "metric_type": "register_with_email_and_password",
                    "latitude": 34.132131,
                    "longitude": 34.12231,
                }
            }
        }
