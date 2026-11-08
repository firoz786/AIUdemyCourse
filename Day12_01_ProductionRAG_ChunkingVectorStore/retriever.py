"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
This module demonstrates alternative/simpler retrieval strategies that
complement the Chroma vector search used in `advanced_rag.py`. It shows
how to compute similarity "by hand" with cosine similarity and plain
keyword overlap, and how to blend semantic + keyword scores into a
single hybrid ranking. These helpers are useful for comparison and
evaluation even though the main pipeline relies on Chroma's own search.
"""
import numpy as np

from embeddings import create_embedding


def cosine_similarity(vector1, vector2):
    """Measure how similar two vectors are, from -1 (opposite) to 1 (identical direction)."""
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    # Cosine similarity = dot product divided by the product of magnitudes.
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def semantic_search(query, chunks, top_k=5):
    """Rank chunks purely by embedding similarity to the query."""
    # Turn the user's query into the same kind of vector as the chunks.
    query_embedding = create_embedding(query)

    results = []
    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "semantic_score": score
        })

    # Highest similarity first, then keep only the best `top_k`.
    results.sort(key=lambda item: item["semantic_score"], reverse=True)
    return results[:top_k]


def keyword_score(query, text):
    """Score the overlap between query words and text words (0 to 1)."""
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())

    if not query_words:
        return 0.0

    # Fraction of query words that also appear in the text.
    matches = query_words & text_words
    return len(matches) / len(query_words)


def hybrid_search(query, chunks, top_k=5, semantic_weight=0.7, keyword_weight=0.3):
    """Rank chunks using a weighted blend of semantic + keyword scores."""
    query_embedding = create_embedding(query)

    results = []
    for chunk in chunks:
        semantic = cosine_similarity(query_embedding, chunk["embedding"])
        keyword = keyword_score(query, chunk["text"])
        # Blend both scores so neither pure semantic drift nor pure
        # keyword matching dominates the final ranking on its own.
        combined = semantic * semantic_weight + keyword * keyword_weight

        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "semantic_score": semantic,
            "keyword_score": keyword,
            "combined_score": combined
        })

    results.sort(key=lambda item: item["combined_score"], reverse=True)
    return results[:top_k]
