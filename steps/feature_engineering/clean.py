from typing import List
from clearml import Task

from application.preprocessing.dispatchers import CleaningDispatcher
from domain.base import NoSQLBaseDocument
from domain.cleaned_documents import CleanedDocument


def clean_documents(raw_documents: List[NoSQLBaseDocument]) -> List[CleanedDocument]:
    cleaned_documents = []
    for document in raw_documents:
        cleaned_document = CleaningDispatcher.dispatch(document)
        cleaned_documents.append(cleaned_document)

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

    task = Task.current_task()
    task.upload_artifact("cleaned_documents", metadata)

    return cleaned_documents
