from typing import List

from clearml import Task

from application import utils
from application.preprocessing.dispatchers import ChunkingDispatcher, EmbeddingDispatcher
from domain.chunks import Chunk
from domain.cleaned_documents import CleanedDocument
from domain.embedded_chunks import EmbeddedChunk


def chunk_and_embed(cleaned_documents: List[CleanedDocument]) -> List[EmbeddedChunk]:
  def _add_chunks_metadata(chunks: List[Chunk], metadata: dict) -> dict:
    for chunk in chunks:
      category = chunk.get_category()
      if category not in metadata:
        metadata[category] = chunk.metadata
      if "authors" not in metadata[category]:
        metadata[category]["authors"] = list()

      metadata[category]["num_chunks"] = metadata[category].get("num_chunks", 0) + 1
      metadata[category]["authors"].append(chunk.author_full_name)

    for value in metadata.values():
      if isinstance(value, dict) and "authors" in value:
        value["authors"] = list(set(value["authors"]))

    return metadata

  def _add_embeddings_metadata(embedded_chunks: List[EmbeddedChunk], metadata: dict) -> dict:
    for embedded_chunk in embedded_chunks:
      category = embedded_chunk.get_category()
      if category not in metadata:
        metadata[category] = embedded_chunk.metadata
      if "authors" not in metadata[category]:
        metadata[category]["authors"] = list()

      metadata[category]["authors"].append(embedded_chunk.author_full_name)

    for value in metadata.values():
      if isinstance(value, dict) and "authors" in value:
        value["authors"] = list(set(value["authors"]))

    return metadata

  metadata = {"chunking": {}, "embedding": {}, "num_documents": len(cleaned_documents)}

  embedded_chunks = []
  for document in cleaned_documents:
    chunks = ChunkingDispatcher.dispatch(document)
    metadata["chunking"] = _add_chunks_metadata(chunks, metadata["chunking"])

    for batched_chunks in utils.misc.batch(chunks, 10):
      batched_embedded_chunks = EmbeddingDispatcher.dispatch(batched_chunks)
      embedded_chunks.extend(batched_embedded_chunks)

  metadata["embedding"] = _add_embeddings_metadata(embedded_chunks, metadata["embedding"])
  metadata["num_chunks"] = len(embedded_chunks)
  metadata["num_embedded_chunks"] = len(embedded_chunks)

  task = Task.current_task()
  task.upload_artifact("embedded_documents", embedded_chunks, metadata=metadata)

  return embedded_chunks
