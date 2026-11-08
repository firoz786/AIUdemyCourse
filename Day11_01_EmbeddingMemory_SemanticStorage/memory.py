"""
Day11_01_EmbeddingMemory_SemanticStorage - memory.py

This file teaches semantic (embedding-based) memory for AI agents: instead
of only remembering the literal text of past conversation turns, it
converts each user/assistant exchange into a numeric vector (an
"embedding") using an embedding model, stores that vector alongside the
text in a local SQLite database, and later retrieves the most relevant
past memories for a new query by comparing embeddings with cosine
similarity -- the same idea behind vector databases used in production
Retrieval-Augmented Generation (RAG) systems.
"""

import json
import sqlite3

import numpy as np
from openai import OpenAI

# Path to the local SQLite file used to persist memories between runs.
DATABASE = "memory.db"

# Client pointed at a local Ollama server, used only to create embeddings
# (turning text into vectors) via the "nomic-embed-text" model.
embedding_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def create_database():
    # Open (or create) the SQLite file and ensure the memories table exists.
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Each row stores one user/assistant exchange plus its embedding
    # (saved as a JSON string, since SQLite has no native vector type).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            assistant_message TEXT,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def create_embedding(text):
    # Ask the embedding model to turn text into a list of floats (a vector)
    # that captures its meaning, so similar meanings end up as similar
    # vectors.
    response = embedding_client.embeddings.create(
        model="nomic-embed-text",
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(vector1, vector2):
    # Cosine similarity measures how similar two vectors' directions are,
    # regardless of magnitude: 1.0 means identical direction (very similar
    # meaning), 0.0 means unrelated.
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    return np.dot(v1, v2) / (
        np.linalg.norm(v1) *
        np.linalg.norm(v2)
    )


def save_memory(user_message, assistant_message):
    # Combine both sides of the exchange so the embedding captures the
    # full context of what was said.
    text = user_message + "\n" + assistant_message

    embedding = create_embedding(text)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Store the raw text plus the embedding (as JSON) for later retrieval.
    cursor.execute(
        """
        INSERT INTO memories
        (
            user_message,
            assistant_message,
            embedding
        )
        VALUES (?, ?, ?)
        """,
        (
            user_message,
            assistant_message,
            json.dumps(embedding)
        )
    )

    connection.commit()
    connection.close()


def search_semantic_memories(
    query,
    top_k=3,
    threshold=0.20
):
    # Turn the search query into a vector using the same embedding model,
    # so it can be compared against stored memory vectors.
    query_embedding = create_embedding(query)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Load every stored memory (a real system would use a vector index
    # instead of scanning all rows, but this keeps the demo simple).
    cursor.execute("""
        SELECT
            user_message,
            assistant_message,
            embedding,
            created_at
        FROM memories
    """)

    rows = cursor.fetchall()

    connection.close()

    results = []

    for (
        user_message,
        assistant_message,
        embedding_json,
        created_at
    ) in rows:

        # Decode the stored embedding back into a list of floats.
        memory_embedding = json.loads(
            embedding_json
        )

        # Compare the query's meaning to this memory's meaning.
        score = cosine_similarity(
            query_embedding,
            memory_embedding
        )

        # Only keep memories that are similar enough to be relevant.
        if score >= threshold:
            results.append({
                "user_message": user_message,
                "assistant_message": assistant_message,
                "created_at": created_at,
                "score": score
            })

    # Show the most relevant memories first.
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]


