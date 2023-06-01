from app.api.metrics import routes
from app.config.database import METRICS_COLLECTION_NAME
from app.main import app
from httpx import AsyncClient
import pytest


def test_create_metric_without_errors(test_app):
    metric = {
        "metric": "register_with_email_and_password",
        "latitude": 34.132131,
        "longitude": 34.12231,
    }

    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201

    body = response.json()
    assert "_id" in body
