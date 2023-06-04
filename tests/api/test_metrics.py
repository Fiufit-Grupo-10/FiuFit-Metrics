from app.api.metrics import routes
from app.config.database import METRICS_COLLECTION_NAME
from app.main import app
from httpx import AsyncClient
import pytest
from app.api.metrics.models import MetricType


def test_create_register_with_email_and_password_metric(test_app):
    metric = {
        "metric": {
            "metric_type": MetricType.register_with_email_and_password,
            "latitude": -36.623237918303765,  # Estas coordenadas correspondes a provincia: La Pampa, departamento: Capital
            "longitude": -64.29505665365905,
        },
    }

    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201

    body = response.json()
    assert body["metric"]["metric_type"] == MetricType.register_with_email_and_password
    assert body["metric"]["geographic_zone"]["province"] == "La Pampa"
    assert body["metric"]["geographic_zone"]["department"] == "Capital"
    assert "_id" in body


def test_create_register_with_federated_identity_metric(test_app):
    metric = {
        "metric": {
            "metric_type": MetricType.register_with_federated_identity,
            "latitude": -36.623237918303765,  # Estas coordenadas correspondes a provincia: La Pampa, departamento: Capital
            "longitude": -64.29505665365905,
        },
    }

    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201
    body = response.json()
    print(body)
    assert body["metric"]["metric_type"] == MetricType.register_with_federated_identity
    assert body["metric"]["geographic_zone"]["province"] == "La Pampa"
    assert body["metric"]["geographic_zone"]["department"] == "Capital"
    assert "_id" in body


def test_create_login_with_federated_identity_metric(test_app):
    metric = {
        "metric": {
            "metric_type": MetricType.login_with_federated_identity,
            "latitude": -36.623237918303765,  # Estas coordenadas correspondes a provincia: La Pampa, departamento: Capital
            "longitude": -64.29505665365905,
        },
    }

    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201

    body = response.json()
    assert body["metric"]["metric_type"] == MetricType.login_with_federated_identity
    assert "_id" in body
