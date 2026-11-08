"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
A tiny evaluation helper used to sanity-check retrieval quality: given
a set of retrieved results and the chunk_id we expected to see, it
checks whether retrieval actually found that expected chunk.
"""


def evaluate_retrieval(results, expected_chunk_id):
    """Return True if `expected_chunk_id` appears among the retrieved results."""
    # Pull out just the chunk ids so we can do a simple membership check.
    retrieved_ids = [result["chunk_id"] for result in results]
    return expected_chunk_id in retrieved_ids

