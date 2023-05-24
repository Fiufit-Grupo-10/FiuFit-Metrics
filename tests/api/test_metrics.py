from app.api.metrics import routes
from app.config.database import TRAININGS_COLLECTION_NAME
from app.main import app
from httpx import AsyncClient
import pytest
