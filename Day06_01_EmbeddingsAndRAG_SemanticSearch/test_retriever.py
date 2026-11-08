"""
Day06_01_EmbeddingsAndRAG_SemanticSearch: a quick manual test of the simple
keyword-based `retrieve` function from retriever.py, showing which document
(and its content) matches a basic search term.
"""

from retriever import retrieve

# Search the knowledge base for a document containing "Artificial".
filename, content = retrieve("Artificial")

print(filename)

print()

print(content)
