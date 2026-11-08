"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
This module is the "vector store" half of the RAG pipeline. It uses
Chroma (a local vector database) to persist chunk embeddings on disk
and to run similarity search over them. Storing embeddings in a real
vector database (instead of an in-memory list) is what makes this
example "production-style": it survives restarts and scales to larger
document collections.
"""
import chromadb

# Create (or reopen) a Chroma database that persists to the local
# "./chroma_db" folder, so embeddings survive between script runs.
client = chromadb.PersistentClient(path="./chroma_db")

# Get or create a single collection named "documents" where all chunk
# embeddings for this course example are stored.
collection = client.get_or_create_collection(name="documents")


def add_chunks(chunks):
    """Upsert a list of embedded chunks into the Chroma collection."""
    documents = []
    embeddings = []
    ids = []
    metadatas = []

    for chunk in chunks:
        # The raw chunk text Chroma will index and return on search.
        documents.append(chunk["text"])
        # The pre-computed embedding vector for this chunk.
        embeddings.append(chunk["embedding"])
        # A unique ID built from the source file name and chunk number,
        # so re-running on the same document updates instead of duplicating.
        ids.append(f'{chunk["source"]}_{chunk["chunk_id"]}')
        # Extra metadata returned alongside search results.
        metadatas.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        })

    # "upsert" inserts new ids or updates existing ones with the same id.
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search(query_embedding, top_k=5):
    """Find the `top_k` chunks whose embeddings are closest to the query."""
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
