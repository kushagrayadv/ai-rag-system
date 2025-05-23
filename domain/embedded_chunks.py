from abc import ABC

from pydantic import UUID4, Field

from domain.types import DataCategory
from .base import VectorBaseDocument


class EmbeddedChunk(VectorBaseDocument, ABC):
  content: str
  embedding: list[float] | None
  platform: str
  document_id: UUID4
  author_id: UUID4
  author_full_name: str
  metadata: dict = Field(default_factory=dict)

  @classmethod
  def to_context(cls, chunks: list["EmbeddedChunk"]) -> str:
    context = ""
    for i, chunk in enumerate(chunks):
      context += f"""
            Chunk {i + 1}:
            Type: {chunk.__class__.__name__}
            Platform: {chunk.platform}
            Author: {chunk.author_full_name}
            Content: {chunk.content}\n
            """

    return context


class EmbeddedRepositoryChunk(EmbeddedChunk):
  name: str
  link: str

  class Config:
    name = "embedded_repositories"
    category = DataCategory.REPOSITORIES
    use_vector_index = True


class EmbeddedVideoChunk(EmbeddedChunk):
  name: str
  link: str

  class Config:
    name = "embedded_videos"
    category = DataCategory.VIDEOS
    use_vector_index = True
