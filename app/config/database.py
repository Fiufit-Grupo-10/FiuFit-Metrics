import os

# import motor.motor_asyncio

MONGO_URL = os.getenv("MONGO_URL", "")
METRICS_COLLECTION_NAME = "users"
DB_NAME = "Metrics"


# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
# database = client.trainers
