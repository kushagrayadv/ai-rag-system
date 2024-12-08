from abc import ABC

from pydantic import UUID4

from .base import VectorBaseDocument
from .types import DataCategory


class CleanedDocument(VectorBaseDocument, ABC):
  content: str
  platform: str
  author_id: UUID4
  author_full_name: str


class CleanedRepositoryDocument(CleanedDocument):
  name: str
  link: str

  class Config:
    name = "cleaned_repositories"
    category = DataCategory.REPOSITORIES
    use_vector_index = False


class CleanedVideoDocument(CleanedDocument):
  name: str
  link: str

  class Config:
    name = "cleaned_videos"
    category = DataCategory.VIDEOS
    use_vector_index = False
