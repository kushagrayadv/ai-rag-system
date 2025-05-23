from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi

from settings import settings


class MongoDatabaseConnector:
  _instance: MongoClient | None = None

  def __new__(cls, *args, **kwargs) -> MongoClient:
    if cls._instance is None:
      try:
        cls._instance = MongoClient(settings.DATABASE_HOST, server_api=ServerApi('1'))
      except ConnectionFailure as e:
        logger.error(f"Couldn't connect to the database: {e!s}")

        raise

    logger.info(f"Connection to MongoDB with URI successful: {settings.DATABASE_HOST}")

    return cls._instance


connection = MongoDatabaseConnector()
