from typing import List
from clearml import Task, Logger

from app.application.preprocessing import CleaningDispatcher
from app.domain.cleaned_documents import CleanedDocument


def clean_documents(documents: List[dict]) -> List[CleanedDocument]:
    task = Task.init(project_name="Document Cleaning", task_name="Clean Documents")
    logger = task.get_logger()

    cleaned_documents = []
    for document in documents:
        cleaned_document = CleaningDispatcher.dispatch(document)
        cleaned_documents.append(cleaned_document)

    metadata = _get_metadata(cleaned_documents)
    logger.report_table(title="Cleaned Documents Metadata", series="metadata", iteration=0, table_plot=metadata)

    return cleaned_documents


def _get_metadata(cleaned_documents: List[CleanedDocument]) -> dict:
    metadata = {"num_documents": len(cleaned_documents)}
    for document in cleaned_documents:
        category = document.get_category()
        if category not in metadata:
            metadata[category] = {}
        if "authors" not in metadata[category]:
            metadata[category]["authors"] = list()

        metadata[category]["num_documents"] = metadata[category].get("num_documents", 0) + 1
        metadata[category]["authors"].append(document.author_full_name)

    for value in metadata.values():
        if isinstance(value, dict) and "authors" in value:
            value["authors"] = list(set(value["authors"]))

    return metadata