"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
This file demonstrates the FIRST step of a production-style Retrieval
Augmented Generation (RAG) pipeline: splitting a long document into
smaller overlapping "chunks" of text. Chunking matters because an LLM
and an embedding model can only process a limited amount of text at a
time, and smaller chunks make retrieval more precise. The overlap
between chunks helps avoid losing context that falls near a chunk
boundary.
"""


def create_chunks(text, source, chunk_size=200, overlap=50):
    """Split `text` into overlapping word-based chunks.

    Args:
        text: The full document text to split.
        source: A label (usually the filename) so each chunk can be
            traced back to the document it came from.
        chunk_size: How many words each chunk should contain.
        overlap: How many words consecutive chunks should share, so we
            don't lose meaning that spans a chunk boundary.
    """
    # Split the document into plain words so we can chunk by word count.
    words = text.split()
    chunks = []

    start = 0
    chunk_id = 0
    # Slide a window of `chunk_size` words across the document.
    while start < len(words):
        end = start + chunk_size
        chunk_text = " ".join(words[start:end])

        # Store the chunk text together with metadata we'll need later
        # for retrieval (which document it came from, and its position).
        chunks.append({
            "text": chunk_text,
            "source": source,
            "chunk_id": chunk_id
        })

        chunk_id += 1
        # Step forward by (chunk_size - overlap) so the next chunk
        # re-reads the last `overlap` words for context continuity.
        start += chunk_size - overlap

    return chunks
