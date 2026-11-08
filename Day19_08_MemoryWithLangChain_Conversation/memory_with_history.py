"""
Day 19.08 - Memory with LangChain (Conversation).

This script shows the simplest way to give a chat model "memory": manually
keep a running list of all messages exchanged so far and send the whole
list back to the model on every call. Unlike memory_demo.py (which calls
the model with isolated, one-off messages), here we build up a `messages`
list, append each new user/assistant turn to it, and pass the full
conversation history back in, so the model can correctly recall earlier
facts like the user's name.
"""

from model import model  # The chat model that will process the conversation history.

# Start the conversation history with the user's first message.
messages = [
    {
        "role": "user",
        "content": "My name is Pankaj."
    }
]

# Send the history (just one message so far) and get the model's reply.
first_response = model.invoke(messages)

# Append the assistant's reply to the history so future calls include it.
messages.append(
    {
        "role": "assistant",
        "content": first_response.content
    }
)

# Append the next user question to the same growing history.
messages.append(
    {
        "role": "user",
        "content": "What is my name?"
    }
)

# Send the FULL history (both previous turns plus the new question) so the
# model has the context needed to recall the name from earlier.
second_response = model.invoke(messages)

print(second_response.content)
