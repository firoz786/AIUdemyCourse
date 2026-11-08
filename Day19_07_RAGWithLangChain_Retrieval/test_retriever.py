"""
Day 19.07 - RAG with LangChain (Retrieval).

Small standalone script to sanity-check the retriever in isolation: it
asks the retriever for documents relevant to "What is MCP?" and prints
each retrieved chunk so you can see what context the RAG chain would use.
"""

from retriever import retriever  # The FAISS-backed retriever built in retriever.py.

# Fetch the chunks of text most relevant to this sample question.
results = retriever.invoke(
    "What is MCP?"
)

# Print each retrieved document's text so we can inspect what was found.
for document in results:
    print("\n--- DOCUMENT ---")
    print(document.page_content)
