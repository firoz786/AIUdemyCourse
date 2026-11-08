"""
Day06_01_EmbeddingsAndRAG_SemanticSearch: a tiny math helper used to compare
two embedding vectors. Cosine similarity measures how similar two vectors'
directions are (1 = identical meaning, 0 = unrelated, -1 = opposite),
regardless of their length - this is the standard way to compare embeddings
for semantic search.
"""

import numpy as np


def cosine_similarity(vector1, vector2):
    """Return the cosine similarity between two embedding vectors."""

    v1 = np.array(vector1)
    v2 = np.array(vector2)

    # Dot product divided by the product of vector magnitudes gives the
    # cosine of the angle between the two vectors.
    return np.dot(v1, v2) / (
        np.linalg.norm(v1) *
        np.linalg.norm(v2)
    )

