"""
Day 19.08 - Memory with LangChain (Conversation).

This script demonstrates that a raw chat model call has NO memory of its
own. It sends two separate, independent messages to the model: first
telling it a name, then asking what that name is. Because each `invoke()`
call is a fresh, stateless request with no shared history, the model has
no way to recall the name from the first call, which is exactly the
problem conversational memory is designed to solve (see
memory_with_history.py for the fix).
"""

from model import model  # The chat model; each invoke() call below is independent/stateless.

# First call: tell the model a fact (the name). The model has no memory, so
# it only "knows" this fact for the duration of this single call.
response = model.invoke(
    "My name is Pankaj."
)

print("First response:")
print(response.content)

# Second call: a brand-new, unrelated request as far as the model is
# concerned - it does NOT remember the previous message, so it typically
# cannot correctly answer "What is my name?" here.
response = model.invoke(
    "What is my name?"
)

print("\nSecond response:")
print(response.content)
