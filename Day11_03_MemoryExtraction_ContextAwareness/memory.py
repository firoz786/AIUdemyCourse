"""
Day 11.3 - Memory Extraction & Context Awareness.

This module gives the agent long-term memory backed by a local SQLite
database. It stores each user/assistant exchange together with a vector
embedding of the text, lets the agent search those memories by meaning
(semantic similarity), and - new in this stage - can also save a single
distilled "fact" (produced by the memory extractor) as its own memory
row, separate from the raw conversation.
"""

import json
import sqlite3

import numpy as np
from openai import OpenAI

# Path to the local SQLite file used to persist memories.
DATABASE = "memory.db"

# Local embedding model served by Ollama (used only to turn text into vectors).
embedding_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def create_database():
    """Create the `memories` table if it doesn't already exist."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

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
    """Convert text into a numeric embedding vector using the local model."""
    response = embedding_client.embeddings.create(
        model="nomic-embed-text",
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(vector1, vector2):
    """Measure how similar two embedding vectors are (1.0 = identical direction)."""
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    return np.dot(v1, v2) / (
        np.linalg.norm(v1) *
        np.linalg.norm(v2)
    )


def save_memory(user_message, assistant_message):
    """Embed and persist one user/assistant exchange as a memory row."""
    text = user_message + "\n" + assistant_message

    # Turn the combined exchange into an embedding we can later compare against.
    embedding = create_embedding(text)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

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
            # Embeddings are stored as JSON text since SQLite has no vector type.
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
    """Return the top matching memories whose similarity to `query` meets
    the threshold, most similar first."""
    # Embed the incoming query so it can be compared to stored memories.
    query_embedding = create_embedding(query)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Load every stored memory; with a small demo database this simple
    # "scan everything" approach is fine (no vector index needed).
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

        # Decode the stored embedding back into a list of numbers.
        memory_embedding = json.loads(
            embedding_json
        )

        # Compare the query's embedding against this memory's embedding.
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

    # Put the most relevant (highest score) memories first.
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]


def save_semantic_memory(fact):
    """Persist a single distilled fact (from the memory extractor) as its
    own memory row, with no assistant reply attached."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Embed just the fact text so it can be matched by future searches.
    embedding = create_embedding(fact)

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
            fact,
            # No assistant reply applies to a distilled fact, so leave it blank.
            "",
            json.dumps(embedding)
        )
    )

    connection.commit()
    connection.close()

