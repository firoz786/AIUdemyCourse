"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
This module wires together the full advanced RAG pipeline for this
course day: chunking, embedding, storing in Chroma, hybrid (semantic +
keyword) scoring, and LLM reranking. `build_rag` ingests a document end
to end, and `retrieve` runs a query through semantic search, keyword
scoring, and reranking to return the best chunks for the generator.
"""
from chunker import create_chunks
from embeddings import embed_chunks, create_embedding
from chroma_store import add_chunks, search as chroma_search
from retriever import keyword_score
from reranker import rerank


def build_rag(text, source):
    """Chunk, embed, and store a document so it can be retrieved later."""
    chunks = create_chunks(text, source=source, chunk_size=200, overlap=50)
    embedded_chunks = embed_chunks(chunks)
    add_chunks(embedded_chunks)
    return embedded_chunks


def retrieve(query, top_k=5):
    """Run the full retrieval pipeline: semantic search -> hybrid scoring -> rerank."""
    # Embed the query once; it's reused for the vector search below.
    query_embedding = create_embedding(query)

    # Ask Chroma for the `top_k` closest chunks by embedding distance.
    semantic_results = chroma_search(query_embedding, top_k=top_k)

    candidates = []
    # Chroma returns results wrapped in a list-of-lists (one list per
    # query embedding); since we only sent one query, we unwrap index [0].
    documents = semantic_results["documents"][0]
    metadatas = semantic_results["metadatas"][0]
    distances = semantic_results["distances"][0]

    for i in range(len(documents)):
        text = documents[i]
        metadata = metadatas[i]
        distance = distances[i]

        # Convert distance (smaller = more similar) into a 0-1 similarity
        # score (larger = more similar) so it's easier to blend below.
        semantic = 1 / (1 + distance)
        keyword = keyword_score(query, text)

        # Blend semantic similarity and keyword overlap into one score,
        # favoring semantic meaning but still rewarding exact word matches.
        combined = 0.7 * semantic + 0.3 * keyword

        candidates.append({
            "text": text,
            "source": metadata["source"],
            "chunk_id": metadata["chunk_id"],
            "semantic_score": semantic,
            "keyword_score": keyword,
            "combined_score": combined
        })

    # Best combined score first, then keep only the top_k candidates.
    candidates.sort(key=lambda item: item["combined_score"], reverse=True)
    candidates = candidates[:top_k]

    # Show which sources/chunks made it through hybrid scoring, before
    # the (slower) LLM reranker narrows things down further.
    print("\nRetrieved Sources Candidates:")
    for candidate in candidates:
        print(f"- {candidate['source']} (chunk {candidate['chunk_id']})")

    # Let the LLM reranker pick the final best 3 chunks to hand to the
    # answer generator.
    return rerank(query, candidates, top_k=3)
