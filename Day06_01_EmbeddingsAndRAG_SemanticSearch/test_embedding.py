"""
Day06_01_EmbeddingsAndRAG_SemanticSearch: defines `create_embedding`, which
calls a local embedding model (via Ollama) to turn a piece of text into a
numeric vector ("embedding") that captures its meaning. This is the building
block used by rag.py and retriever.py to compare text for semantic
similarity.
"""

from openai import OpenAI

# Client pointed at a local Ollama server, which serves the embedding model.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def create_embedding(content):
    """Convert a piece of text into an embedding vector."""
    embedding1 = client.embeddings.create(
    model="nomic-embed-text",
    input=content
    ).data[0].embedding
    return embedding1





