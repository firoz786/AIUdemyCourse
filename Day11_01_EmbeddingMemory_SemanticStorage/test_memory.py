"""
Day11_01_EmbeddingMemory_SemanticStorage - test_memory.py

A simple manual walkthrough script for the semantic memory module
(memory.py). It initializes the SQLite memory database, saves a few
sample conversation exchanges (each gets embedded automatically), then
searches for memories relevant to "What is my name" to demonstrate that
semantic search finds the right memory even without an exact keyword
match.
"""

from memory import (
    create_database,
    save_memory,
    search_semantic_memories
)

# Step 1: Make sure the memories table exists before we use it.
create_database()

# Step 2: Save a few sample conversation turns; each is embedded and
# stored so it can be retrieved later by meaning, not just exact text.
save_memory(
    "My name is Pankaj.",
    "Nice to meet you, Pankaj."
)

save_memory(
    "I am learning Python.",
    "Python is useful for AI development."
)

save_memory(
    "I am learning about MCP.",
    "MCP allows AI applications to use tools."
)

# Step 3: Search for memories relevant to this query using embeddings and
# cosine similarity, rather than exact keyword matching.
results = search_semantic_memories(
    "What is my name"
)

print("\nRelevant Memories")
print("-----------------")

for result in results:
    print("\nScore:", result["score"])
    print("User:", result["user_message"])
    print("Assistant:", result["assistant_message"])

