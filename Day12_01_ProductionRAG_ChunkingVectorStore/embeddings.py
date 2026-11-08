"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
This module wraps the embedding model used throughout the RAG
pipeline. An "embedding" turns text into a list of numbers (a vector)
that captures its meaning, so chunks of text can be compared by
similarity instead of exact keyword matches. Here we talk to a local
Ollama server (which exposes an OpenAI-compatible API) using the
`nomic-embed-text` embedding model.
"""
from openai import OpenAI

# Point the OpenAI client at a local Ollama server instead of the real
# OpenAI API. The api_key value is just a placeholder; Ollama ignores it.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# The embedding model Ollama will run for every embedding request.
MODEL = "nomic-embed-text"


def create_embedding(text):
    """Turn a single string of text into an embedding vector."""
    response = client.embeddings.create(
        model=MODEL,
        input=text
    )
    # The API returns a list of embeddings; we only sent one input, so
    # grab the first (and only) result.
    return response.data[0].embedding


def embed_chunks(chunks):
    """Add an "embedding" vector to every chunk dictionary in `chunks`."""
    embedded_chunks = []

    for chunk in chunks:
        # Compute the embedding for this chunk's text only.
        embedding = create_embedding(chunk["text"])

        # Keep all original chunk metadata and attach the new embedding.
        embedded_chunks.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "embedding": embedding
        })

    return embedded_chunks

