from typing import Any

from libs.llm import vector


async def add_docs(
    documents: list[str],
    embeddings: list[Any],
    metadatas: list[dict[str, str]],
    ids: list[int],
) -> None:
    vector.add(documents=documents,
               embeddings=embeddings,
               metadatas=metadatas,
               ids=ids)
