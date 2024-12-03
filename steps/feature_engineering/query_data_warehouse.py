from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from clearml import Task
from loguru import logger

from application import utils
from domain.base.nosql import NoSQLBaseDocument
from domain.documents import Document, RepositoryDocument, UserDocument, VideoDocument


def query_data_warehouse(author_full_names: List[str]) -> List[NoSQLBaseDocument]:
  def fetch_all_data(user: UserDocument) -> dict[str, List[NoSQLBaseDocument]]:
    user_id = str(user.id)
    with ThreadPoolExecutor() as executor:
      future_to_query = {
        executor.submit(__fetch_repositories, user_id): "repositories",
        executor.submit(__fetch_videos, user_id): "videos"
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

  def __fetch_repositories(user_id) -> List[NoSQLBaseDocument]:
    return RepositoryDocument.bulk_find(author_id=user_id)

  def __fetch_videos(user_id) -> List[NoSQLBaseDocument]:
    return VideoDocument.bulk_find(author_id=user_id)

  def _get_metadata(documents: List[Document]) -> dict:
    metadata = {
      "num_documents": len(documents),
    }
    for document in documents:
      collection = document.get_collection_name()
      if collection not in metadata:
        metadata[collection] = {}
      if "authors" not in metadata[collection]:
        metadata[collection]["authors"] = list()

      metadata[collection]["num_documents"] = metadata[collection].get("num_documents", 0) + 1
      metadata[collection]["authors"].append(document.author_full_name)

    for value in metadata.values():
      if isinstance(value, dict) and "authors" in value:
        value["authors"] = list(set(value["authors"]))

    return metadata

  documents = []
  authors = []
  for author_full_name in author_full_names:
    logger.info(f"Querying data warehouse for user: {author_full_name}")

    first_name, last_name = utils.split_user_full_name(author_full_name)
    logger.info(f"First name: {first_name}, Last name: {last_name}")
    user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)
    authors.append(user)

    results = fetch_all_data(user)
    user_documents = [doc for query_result in results.values() for doc in query_result]

    documents.extend(user_documents)

  metadata = _get_metadata(documents)
  task = Task.current_task()
  task.upload_artifact("user_documents", documents, metadata=metadata)

  return documents
