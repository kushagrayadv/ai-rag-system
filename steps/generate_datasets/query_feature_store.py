from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger
from qdrant_client.http import exceptions
from typing_extensions import Annotated

from domain.base.nosql import NoSQLBaseDocument
from domain.cleaned_documents import (
  CleanedDocument,
  CleanedRepositoryDocument, CleanedVideoDocument
)


def query_feature_store() -> Annotated[list, "queried_cleaned_documents"]:
  logger.info("Querying feature store.")

  def fetch_all_data() -> dict[str, list[NoSQLBaseDocument]]:
    with ThreadPoolExecutor() as executor:
      future_to_query = {
        executor.submit(
          __fetch_repositories,
        ): "repositories",
        executor.submit(
          __fetch_videos,
        ): "videos",
      }

      results = {}
      for future in as_completed(future_to_query):
        query_name = future_to_query[future]
        try:
          results[query_name] = future.result()
        except Exception:
          logger.exception(f"'{query_name}' request failed.")

          results[query_name] = []

    return results

  def __fetch_repositories() -> list[CleanedDocument]:
    return __fetch(CleanedRepositoryDocument)

  def __fetch_videos() -> list[CleanedDocument]:
    return __fetch(CleanedVideoDocument)

  def __fetch(cleaned_document_type: type[CleanedDocument], limit: int = 1) -> list[CleanedDocument]:
    try:
      cleaned_documents, next_offset = cleaned_document_type.bulk_find(limit=limit)
    except exceptions.UnexpectedResponse:
      return []

    while next_offset:
      documents, next_offset = cleaned_document_type.bulk_find(limit=limit, offset=next_offset)
      cleaned_documents.extend(documents)

    return cleaned_documents

  results = fetch_all_data()

  cleaned_documents = [doc for query_result in results.values() for doc in query_result]

  return cleaned_documents
