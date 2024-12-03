from typing import List

from loguru import logger

from application import utils
from domain.base import VectorBaseDocument


def load_to_vector_db(documents: List[VectorBaseDocument]) -> bool:
  logger.info(f"Loading {len(documents)} documents into the vector database.")

  grouped_documents = VectorBaseDocument.group_by_class(documents)
  for document_class, docs in grouped_documents.items():
    logger.info(f"Loading documents into {document_class.get_collection_name()}")
    for documents_batch in utils.misc.batch(docs, size=4):
      try:
        document_class.bulk_insert(documents_batch)
      except Exception as e:
        logger.error(
          f"Failed to insert documents into {document_class.get_collection_name()}: {str(e)}",

        )
        return False

  return True
