"""
Day06_01_EmbeddingsAndRAG_SemanticSearch: helper functions for loading the
knowledge base documents used by the RAG pipeline. `load_documents` reads
every .txt file from the `knowledge/` folder, while `retrieve` offers a much
simpler (non-embedding) way to find a document: plain substring search. This
contrasts with rag.py's embedding-based semantic search.
"""

from pathlib import Path


def load_documents():
    """Load every .txt file in the knowledge/ folder into a dict."""

    documents = {}

    folder = Path("knowledge")

    # Read each text file's content, keyed by its filename.
    for file in folder.glob("*.txt"):

        documents[file.name] = file.read_text(
            encoding="utf-8"
        )

    return documents


def retrieve(question):
    """Find the first document whose text contains the question (simple
    keyword search, unlike the embedding-based search used in rag.py)."""

    documents = load_documents()

    question = question.lower()

    # Return the first document whose content contains the question text
    # (case-insensitive substring match).
    for filename, content in documents.items():

        if question in content.lower():

            return filename, content

    return None, None
