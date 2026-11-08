"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
This module implements an LLM-based "reranker": a second-pass filter
that asks the chat model to score how relevant each retrieved chunk
really is to the query, then keeps only the best ones. Rerankers
improve RAG quality because the initial vector/keyword search can
surface chunks that are only superficially similar; the LLM reranker
provides a more semantic, second opinion before generation.
"""
from openai import OpenAI

# Reuse the same local Ollama chat model used for answer generation.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "qwen3:1.7b"


def rerank(query, candidates, top_k=3):
    """Ask the LLM to score each candidate chunk's relevance, then keep the top ones."""
    scored = []

    for candidate in candidates:
        # Ask the model to grade relevance of this one chunk from 0-100.
        prompt = f"""
You are a document relevance evaluator.

User Query:
{query}

Document:
{candidate["text"]}

Give a relevance score from 0 to 100.

100 = directly answers the query
0 = completely irrelevant

Return ONLY the number.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        score_text = response.choices[0].message.content.strip()

        # The model should return a plain number; fall back to 0 if it
        # replies with something we can't parse (defensive coding).
        try:
            score = float(score_text)
        except ValueError:
            score = 0

        # Keep all original candidate fields plus the new rerank score.
        scored.append({**candidate, "rerank_score": score})

    # Highest-scoring chunks first, then keep only the best `top_k`.
    scored.sort(key=lambda item: item["rerank_score"], reverse=True)
    return scored[:top_k]


