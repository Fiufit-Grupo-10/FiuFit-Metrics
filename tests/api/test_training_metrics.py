from app.main import app
from httpx import AsyncClient
import pytest


@pytest.mark.anyio
async def test_put_metrics_new_training(test_app):
    metric = {
        "metric": {
            "metric_type": "usage",
            "fulfilled_counter": 20,
            "completed_counter": 10,
        }
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "metrics/trainings/c59710ef-f5d0-41ba-a787-ad8eb739ef4c", json=metric
        )

    assert response.status_code == 201
    body = response.json()
    assert "_id" in body


@pytest.mark.anyio
async def test_put_metrics_usage(test_app):
    metric = {
        "metric": {
            "metric_type": "score",
            "favourite_counter": 15,
            "review_counter": 0,
            "review_average": 0,
        }
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "metrics/trainings/c59710ef-f5d0-41ba-a787-ad8eb739ef4c", json=metric
        )

    assert response.status_code == 201
    id = response.json()["_id"]

    metric = {
        "metric": {
            "metric_type": "usage",
            "fulfilled_counter": 20,
            "completed_counter": 10,
        }
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "metrics/trainings/c59710ef-f5d0-41ba-a787-ad8eb739ef4c", json=metric
        )

    assert response.status_code == 200
    expected = {
        "_id": id,
        "training_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "favourite_counter": 15,
        "review_counter": 0,
        "completed_counter": 10,
        "fulfilled_counter": 20,
        "review_average": 0,
    }
    assert response.json() == expected


@pytest.mark.anyio
async def test_put_metrics_score(test_app):
    metric = {
        "metric": {
            "metric_type": "usage",
            "fulfilled_counter": 20,
            "completed_counter": 10,
        }
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "metrics/trainings/c59710ef-f5d0-41ba-a787-ad8eb739ef4c", json=metric
        )

    assert response.status_code == 201
    id = response.json()["_id"]

    metric = {
        "metric": {
            "metric_type": "score",
            "favourite_counter": 1,
            "review_counter": 10,
            "review_average": 3.5,
        }
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "metrics/trainings/c59710ef-f5d0-41ba-a787-ad8eb739ef4c", json=metric
        )

    assert response.status_code == 200
    expected = {
        "_id": id,
        "training_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "favourite_counter": 1,
        "review_counter": 10,
        "completed_counter": 10,
        "fulfilled_counter": 20,
        "review_average": 3.5,
    }
    assert response.json() == expected


@pytest.mark.anyio
async def test_get_metrics(test_app):
    metric = {
        "metric": {
            "metric_type": "usage",
            "fulfilled_counter": 20,
            "completed_counter": 10,
        }
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "metrics/trainings/c59710ef-f5d0-41ba-a787-ad8eb739ef4c", json=metric
        )

    assert response.status_code == 201
    id = response.json()["_id"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "metrics/trainings/c59710ef-f5d0-41ba-a787-ad8eb739ef4c"
        )

    assert response.status_code == 200
    expected = {
        "_id": id,
        "training_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "favourite_counter": 0,
        "review_counter": 0,
        "completed_counter": 10,
        "fulfilled_counter": 20,
        "review_average": 0,
    }
    assert response.json() == expected


@pytest.mark.anyio
async def test_get_metrics_fail(test_app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "metrics/trainings/c59710ef-f5d0-41ba-a787-ad8eb739ef4c"
        )

    assert response.status_code == 200
