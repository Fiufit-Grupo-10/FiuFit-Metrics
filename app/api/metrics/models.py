from email.policy import default
from enum import Enum
import string
from typing import Tuple
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Literal
from datetime import datetime
import httpx


class TotalMetricsResponse(BaseModel):
    register_with_email_and_password: int | None = Field(default=0)
    register_with_federated_identity: int | None = Field(default=0)
    login_with_email_and_password: int | None = Field(default=0)
    login_with_federated_identity: int | None = Field(default=0)
    blocked_user: int | None = Field(default=0)
    password_recover: int | None = Field(default=0)

    class Config:
        schema_extra = {
            "register_with_email_and_password": 10,
            "register_with_federated_identity": 3,
            "login_with_email_and_password": 2,
            "login_with_federated_identity": 20,
            "blocked_user": 40,
            "password_recover": 1,
        }


class Position(BaseModel):
    latitude: float = Field(...)
    longitude: float = Field(...)


class MetricType(str, Enum):
    register_with_email_and_password = "register_with_email_and_password"
    register_with_federated_identity = "register_with_federated_identity"
    login_with_email_and_password = "login_with_email_and_password"
    login_with_federated_identity = "login_with_federated_identity"
    blocked_user = "blocked_user"
    password_recover = "password_recover"


class UserWithGeographicZone(BaseModel):
    province: str
    department: str


class NewUser(BaseModel):
    metric_type: Literal[
        MetricType.register_with_email_and_password,
        MetricType.register_with_federated_identity,
    ]
    geographic_zone: UserWithGeographicZone | None

    def __init__(self, **data) -> None:
        (
            lat,
            lon,
        ) = (data.get("latitude"), data.get("longitude"))
        position = Position(latitude=lat, longitude=lon)
        url = f"https://apis.datos.gob.ar/georef/api/ubicacion?lat={position.latitude}&lon={position.longitude}"
        response = httpx.get(url)
        json_data = response.json()
        department = json_data["ubicacion"]["departamento"]["nombre"]
        province = json_data["ubicacion"]["provincia"]["nombre"]

        data["geographic_zone"] = UserWithGeographicZone(
            province=province,
            department=department,
        )

        super().__init__(**data)


class Login(BaseModel):
    metric_type: Literal[
        MetricType.login_with_federated_identity,
        MetricType.login_with_email_and_password,
    ]


class BlockedUser(BaseModel):
    metric_type: Literal[MetricType.blocked_user]


class PasswordRecover(BaseModel):
    metric_type: Literal[MetricType.password_recover]


class UserMetric(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    updated: datetime = Field(default_factory=datetime.utcnow)
    metric: NewUser | Login | BlockedUser | PasswordRecover = Field(
        ..., discriminator="metric_type"
    )

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "metric": {
                    "metric_type": "register_with_email_and_password",
                    "latitude": -34.59854399794779,
                    "longitude": -58.412105357951795,
                }
            },
        }
