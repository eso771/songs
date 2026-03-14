from motor.motor_asyncio import AsyncIOMotorClient

from Song.cinfig import Cinfig

from Song.logger import LOGGER

LOGGER.info("Connecting to your Mongo Database...")
try:
    _mongo_async_ = AsyncIOMotorClient(Config.MONGODB_URI)
    mongodb = _mongo_async_.Inflex   # <-- burda "Inflex" əslində sənin DB adındır
    LOGGER.info("Connected to your Mongo Database.")
except Exception as e:
    LOGGER.error(f"Failed to connect to your Mongo Database: {e}")
    exit()
