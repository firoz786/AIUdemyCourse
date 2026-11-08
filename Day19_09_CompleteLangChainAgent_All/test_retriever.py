"""
Day 19.09 - Quick manual test for the RAG retriever.

This script is a tiny smoke test / demo: it runs a sample question through
the shared `retriever` (from retriever.py) and prints out every matching
document chunk it finds, so you can eyeball whether the retriever is
returning sensible results from notes.txt.
"""

from retriever import retriever

# Ask the retriever for chunks relevant to this sample question.
results = retriever.invoke(
    "What is MCP?"
)

# Print each retrieved chunk so we can manually inspect the results.
for document in results:
    print("\n--- DOCUMENT ---")
    print(document.page_content)
