from abc import ABC

from pydantic import UUID4, Field

from domain.types import DataCategory
from .base import VectorBaseDocument


class Chunk(VectorBaseDocument, ABC):
  content: str
  platform: str
  document_id: UUID4
  author_id: UUID4
  author_full_name: str
  metadata: dict = Field(default_factory=dict)


class RepositoryChunk(Chunk):
  name: str
  link: str

  class Config:
    category = DataCategory.REPOSITORIES


class VideoChunk(Chunk):
  name: str
  link: str

  class Config:
    category = DataCategory.VIDEOS
