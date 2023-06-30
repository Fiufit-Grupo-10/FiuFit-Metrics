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


def test_create_register_with_federated_identity(test_app):
    metric = {
        "metric": {
            "metric_type": MetricType.register_with_federated_identity,
            "latitude": -36.623237918303765,
            "longitude": -64.29505665365905,
        },
    }

    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201

    body = response.json()
    assert body["metric"]["metric_type"] == MetricType.register_with_federated_identity
    assert body["metric"]["geographic_zone"]["province"] == "La Pampa"
    assert body["metric"]["geographic_zone"]["department"] == "Capital"
    assert "_id" in body


def test_get_geographical_totals_normal_register(test_app):
    response = test_app.get(
        "/metrics/locations?register_type=register_with_email_and_password"
    )
    assert response.status_code == 200

    body = response.json()
    provinces = body["provinces"]
    departments = body["departments"]
    assert provinces[0]["province"] == "La Pampa"
    assert provinces[0]["counter"] == 1
    assert departments[0]["department"] == "Capital"
    assert departments[0]["counter"] == 1


def test_get_geographical_totals_federated_register(test_app):
    response = test_app.get(
        "/metrics/locations?register_type=register_with_email_and_password"
    )
    assert response.status_code == 200

    body = response.json()
    provinces = body["provinces"]
    departments = body["departments"]
    assert provinces[0]["province"] == "La Pampa"
    assert provinces[0]["counter"] == 1
    assert departments[0]["department"] == "Capital"
    assert departments[0]["counter"] == 1


def test_get_total_metrics(test_app):
    response = test_app.get("/metrics/totals")
    assert response.status_code == 200

    body = response.json()

    assert body["register_with_email_and_password"] == 1
    assert body["register_with_federated_identity"] == 1
    assert body["login_with_email_and_password"] == 0
    assert body["login_with_federated_identity"] == 0
    assert body["blocked_user"] == 0
    assert body["password_recover"] == 0


def test_create_login_with_email_and_password(test_app):
    metric = {
        "metric": {
            "metric_type": MetricType.login_with_email_and_password,
        },
    }
    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201

    body = response.json()
    assert body["metric"]["metric_type"] == MetricType.login_with_email_and_password
    assert "_id" in body


def test_create_login_with_federated_identity(test_app):
    metric = {
        "metric": {
            "metric_type": MetricType.login_with_federated_identity,
        },
    }
    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201

    body = response.json()
    assert body["metric"]["metric_type"] == MetricType.login_with_federated_identity
    assert "_id" in body


def test_create_blocked_user(test_app):
    metric = {
        "metric": {
            "metric_type": MetricType.blocked_user,
        },
    }
    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201

    body = response.json()
    assert body["metric"]["metric_type"] == MetricType.blocked_user
    assert "_id" in body


def test_create_password_recover(test_app):
    metric = {
        "metric": {
            "metric_type": MetricType.password_recover,
        },
    }
    response = test_app.post("/metrics", json=metric)
    assert response.status_code == 201

    body = response.json()
    assert body["metric"]["metric_type"] == MetricType.password_recover
    assert "_id" in body


def test_get_normal_register_metric(test_app):
    response = test_app.get("/metrics?metric_type=register_with_email_and_password")
    assert response.status_code == 200
    body = response.json()

    assert body[0]["metric"]["metric_type"] == "register_with_email_and_password"
    assert body[0]["metric"]["geographic_zone"]["province"] == "La Pampa"
    assert body[0]["metric"]["geographic_zone"]["department"] == "Capital"


# def test_get_federated_register_metric(test_app):
#     response = test_app.get("/metrics?metric_type=register_with_federated_indetity")
#     assert response.status_code == 200
#     body = response.json()
#     print(body)
#     assert 1 == 2


def test_get_blocked_user_metric(test_app):
    response = test_app.get("/metrics?metric_type=blocked_user")
    assert response.status_code == 200
    body = response.json()
    assert body[0]["metric"]["metric_type"] == "blocked_user"


# def test_get_password_recover_metric(test_app):
#     response = test_app.get("/metrics?metric_type=passowrd_recover")
#     assert response.status_code == 200
#     body = response.json()
#     print(body)
#     assert 1 == 2
