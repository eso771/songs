from motor.motor_asyncio import AsyncIOMotorClient

from cinfig import Cinfig

from Song.logger import LOGGER

LOGGER.info("Connecting to your Mongo Database...")
try:
    _mongo_async_ = AsyncIOMotorClient(Cinfig.MONGODB_URI)
    mongodb = _mongo_async_.Inflex
    LOGGER.info("Connected to your Mongo Database.")
except Exception as e:
    LOGGER.error(f"Failed to connect to your Mongo Database: {e}")
    exit()
