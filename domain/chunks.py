from abc import ABC
from typing import Optional

from pydantic import UUID4, Field

from base import VectorBaseDocument
from domain.types import DataCategory


class Chunk(VectorBaseDocument, ABC):
    content: str
    platform: str
    document_id: UUID4
    author_id: UUID4
    author_full_name: str
    metadata: dict = Field(default_factory=dict)


class PostChunk(Chunk):
    image: Optional[str] = None

    class Config:
        category = DataCategory.POSTS


class ArticleChunk(Chunk):
    link: str

    class Config:
        category = DataCategory.ARTICLES


class RepositoryChunk(Chunk):
    name: str
    link: str

    class Config:
        category = DataCategory.REPOSITORIES


class VideoChunk(Chunk):
    name: str
    link: str
    description: Optional[str] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    transcript: Optional[str] = None

    class Config:
        category = DataCategory.VIDEOS