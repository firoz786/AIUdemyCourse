"""
Day 11.3 - Memory Extraction & Context Awareness.

A small standalone script to manually verify the new memory extractor:
it feeds one sample user/assistant exchange (a one-off "what time is
it?" question, which should NOT be remembered) into `extract_memory` and
prints whatever fact (or "NONE") comes back.
"""

from memory_extractor import extract_memory

# A throwaway exchange - the extractor should decide there's nothing
# worth remembering long-term here and return "NONE".
memory = extract_memory(
    "What is the current time?",
    "The current time is 10 PM."
)

print("Extracted Memory:")
print(memory)

