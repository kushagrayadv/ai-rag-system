from loguru import logger

from domain.base import NoSQLBaseDocument, VectorBaseDocument
from domain.types import DataCategory
from .chunking_data_handlers import (
  ChunkingDataHandler,
  RepositoryChunkingHandler,
  VideoChunkingHandler,
)
from .cleaning_data_handlers import (
  CleaningDataHandler,
  RepositoryCleaningHandler,
  VideoCleaningHandler,
)
from .embedding_data_handlers import (
  EmbeddingDataHandler,
  QueryEmbeddingHandler,
  RepositoryEmbeddingHandler,
  VideoEmbeddingHandler,
)


class CleaningHandlerFactory:
  @staticmethod
  def create_handler(data_category: DataCategory) -> CleaningDataHandler:
    if data_category == DataCategory.REPOSITORIES:
      return RepositoryCleaningHandler()
    elif data_category == DataCategory.VIDEOS:
      return VideoCleaningHandler()
    else:
      raise ValueError("Unsupported data type")


class CleaningDispatcher:
  cleaning_factory = CleaningHandlerFactory()

  @classmethod
  def dispatch(cls, data_model: NoSQLBaseDocument) -> VectorBaseDocument:
    data_category = DataCategory(data_model.get_collection_name())
    handler = cls.cleaning_factory.create_handler(data_category)
    clean_model = handler.clean(data_model)

    logger.info(
      "Document cleaned successfully.",
      data_category=data_category,
      cleaned_content_len=len(clean_model.content),
    )

    return clean_model


class ChunkingHandlerFactory:
  @staticmethod
  def create_handler(data_category: DataCategory) -> ChunkingDataHandler:
    if data_category == DataCategory.REPOSITORIES:
      return RepositoryChunkingHandler()
    elif data_category == DataCategory.VIDEOS:
      return VideoChunkingHandler()
    else:
      raise ValueError("Unsupported data type")


class ChunkingDispatcher:
  cleaning_factory = ChunkingHandlerFactory

  @classmethod
  def dispatch(cls, data_model: VectorBaseDocument) -> list[VectorBaseDocument]:
    data_category = data_model.get_category()
    handler = cls.cleaning_factory.create_handler(data_category)
    chunk_models = handler.chunk(data_model)

    logger.info(
      "Document chunked successfully.",
      num=len(chunk_models),
      data_category=data_category,
    )

    return chunk_models


class EmbeddingHandlerFactory:
  @staticmethod
  def create_handler(data_category: DataCategory) -> EmbeddingDataHandler:
    if data_category == DataCategory.QUERIES:
      return QueryEmbeddingHandler()
    elif data_category == DataCategory.REPOSITORIES:
      return RepositoryEmbeddingHandler()
    elif data_category == DataCategory.VIDEOS:
      return VideoEmbeddingHandler()
    else:
      raise ValueError("Unsupported data type")


class EmbeddingDispatcher:
  cleaning_factory = EmbeddingHandlerFactory

  @classmethod
  def dispatch(
    cls, data_model: VectorBaseDocument | list[VectorBaseDocument]
  ) -> VectorBaseDocument | list[VectorBaseDocument]:
    is_list = isinstance(data_model, list)
    if not is_list:
      data_model = [data_model]

    if len(data_model) == 0:
      return []

    data_category = data_model[0].get_category()
    assert all(
      data_model.get_category() == data_category for data_model in data_model
    ), "Data models must be of the same category."
    handler = cls.cleaning_factory.create_handler(data_category)

    embedded_chunk_model = handler.embed_batch(data_model)

    if not is_list:
      embedded_chunk_model = embedded_chunk_model[0]

    logger.info(
      "Data embedded successfully.",
      data_category=data_category,
    )

    return embedded_chunk_model
