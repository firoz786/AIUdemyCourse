"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
This is the entry point that ties the whole Day12 RAG pipeline
together into an interactive chat loop. It loads a sample document,
builds the RAG knowledge base (chunk -> embed -> store), and then lets
the user ask questions in a terminal loop, printing the retrieved
sources and the generated answer for each query.
"""
from pathlib import Path

from advanced_rag import build_rag, retrieve
from generator import generate_answer

# The sample document this demo will ingest and answer questions about.
DOCUMENT_PATH = Path("documents") / "python.txt"


def main():
    # Read the sample document from disk as plain text.
    text = DOCUMENT_PATH.read_text(encoding="utf-8")

    print("Building RAG knowledge base...")
    # Chunk + embed + store the document once, before the chat loop starts.
    build_rag(text, DOCUMENT_PATH.name)

    print("\nAdvanced RAG is ready.")

    while True:
        try:
            # Ask the user for a question; Ctrl+C/Ctrl+D should exit cleanly.
            query = input("\nYou : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
            break

        # Let the user type "exit" or "quit" to leave the chat loop.
        if query.lower() in {"exit", "quit"}:
            break

        # Run the full retrieve pipeline (hybrid search + rerank).
        results = retrieve(query, top_k=5)

        print("\nRetrieved Sources Ranking:")
        for result in results:
            print(f"- {result['source']} (chunk {result['chunk_id']})")

        # Generate the final answer grounded in the retrieved chunks.
        answer = generate_answer(query, results)

        print("\nRAG :")
        print(answer)


if __name__ == "__main__":
    main()


