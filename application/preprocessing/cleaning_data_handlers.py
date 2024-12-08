from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.cleaned_documents import (
  CleanedDocument,
  CleanedRepositoryDocument,
  CleanedVideoDocument,
)
from domain.documents import (
  Document,
  RepositoryDocument,
  VideoDocument,
)
from .operations import clean_text

DocumentT = TypeVar("DocumentT", bound=Document)
CleanedDocumentT = TypeVar("CleanedDocumentT", bound=CleanedDocument)


class CleaningDataHandler(ABC, Generic[DocumentT, CleanedDocumentT]):
  """
  Abstract class for all cleaning data handlers.
  All data transformations logic for the cleaning step is done here
  """

  @abstractmethod
  def clean(self, data_model: DocumentT) -> CleanedDocumentT:
    pass


class RepositoryCleaningHandler(CleaningDataHandler):
  def clean(self, data_model: RepositoryDocument) -> CleanedRepositoryDocument:
    return CleanedRepositoryDocument(
      id=data_model.id,
      content=clean_text(" #### ".join(data_model.content.values())),
      platform=data_model.platform,
      name=data_model.name,
      link=data_model.link,
      author_id=data_model.author_id,
      author_full_name=data_model.author_full_name,
    )


class VideoCleaningHandler(CleaningDataHandler):
  def clean(self, data_model: VideoDocument) -> CleanedVideoDocument:
    return CleanedVideoDocument(
      id=data_model.id,
      content=clean_text(" #### ".join(data_model.content.values())),
      platform=data_model.platform,
      name=data_model.name,
      link=data_model.link,
      author_id=data_model.author_id,
      author_full_name=data_model.author_full_name,
    )
