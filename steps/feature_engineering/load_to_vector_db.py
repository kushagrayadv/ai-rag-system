from loguru import logger
from typing import List
from clearml import Task, Logger

from app import utils
from domain.base import VectorBaseDocument

@Task.add_function
def load_to_vector_db(documents: List[VectorBaseDocument]) -> bool:
    task = Task.current_task()
    logger = task.get_logger()

    logger.report_text(f"Loading {len(documents)} documents into the vector database.")

    grouped_documents = VectorBaseDocument.group_by_class(documents)
    for document_class, docs in grouped_documents.items():
        logger.report_text(f"Loading documents into {document_class.get_collection_name()}")
        for documents_batch in utils.misc.batch(docs, size=4):
            try:
                document_class.bulk_insert(documents_batch)
            except Exception as e:
                logger.report_text(
                    f"Failed to insert documents into {document_class.get_collection_name()}: {str(e)}",
                    level=Logger.ERROR
                )
                return False

    return True