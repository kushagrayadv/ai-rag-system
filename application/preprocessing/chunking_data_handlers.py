import hashlib
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from domain.chunks import Chunk, RepositoryChunk, VideoChunk
from domain.cleaned_documents import (
  CleanedDocument,
  CleanedRepositoryDocument,
  CleanedVideoDocument,
)
from .operations import chunk_text

CleanedDocumentT = TypeVar("CleanedDocumentT", bound=CleanedDocument)
ChunkT = TypeVar("ChunkT", bound=Chunk)


class ChunkingDataHandler(ABC, Generic[CleanedDocumentT, ChunkT]):
  """
  Abstract class for all Chunking data handlers.
  All data transformations logic for the chunking step is done here
  """

  @property
  def metadata(self) -> dict:
    return {
      "chunk_size": 500,
      "chunk_overlap": 50,
    }

  @abstractmethod
  def chunk(self, data_model: CleanedDocumentT) -> list[ChunkT]:
    pass


class RepositoryChunkingHandler(ChunkingDataHandler):
  @property
  def metadata(self) -> dict:
    return {
      "chunk_size": 1500,
      "chunk_overlap": 100,
    }

  def chunk(self, data_model: CleanedRepositoryDocument) -> list[RepositoryChunk]:
    data_models_list = []

    cleaned_content = data_model.content
    chunks = chunk_text(
      cleaned_content, chunk_size=self.metadata["chunk_size"], chunk_overlap=self.metadata["chunk_overlap"]
    )

    for chunk in chunks:
      chunk_id = hashlib.md5(chunk.encode()).hexdigest()
      model = RepositoryChunk(
        id=UUID(chunk_id, version=4),
        content=chunk,
        platform=data_model.platform,
        name=data_model.name,
        link=data_model.link,
        document_id=data_model.id,
        author_id=data_model.author_id,
        author_full_name=data_model.author_full_name,
        metadata=self.metadata,
      )
      data_models_list.append(model)

    return data_models_list


class VideoChunkingHandler(ChunkingDataHandler):
  @property
  def metadata(self) -> dict:
    return {
      "chunk_size": 1500,
      "chunk_overlap": 100,
    }

  def chunk(self, data_model: CleanedVideoDocument) -> list[VideoChunk]:
    data_models_list = []

    cleaned_content = data_model.content
    chunks = chunk_text(
      cleaned_content, chunk_size=self.metadata["chunk_size"], chunk_overlap=self.metadata["chunk_overlap"]
    )

    for chunk in chunks:
      chunk_id = hashlib.md5(chunk.encode()).hexdigest()
      model = VideoChunk(
        id=UUID(chunk_id, version=4),
        content=chunk,
        platform=data_model.platform,
        name=data_model.name,
        link=data_model.link,
        document_id=data_model.id,
        author_id=data_model.author_id,
        author_full_name=data_model.author_full_name,
        metadata=self.metadata,
      )
      data_models_list.append(model)

    return data_models_list
