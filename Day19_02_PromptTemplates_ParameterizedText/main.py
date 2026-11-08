"""
Day 19.02 - Prompt Templates (Parameterized Text) - using a template.

Demonstrates LangChain's ChatPromptTemplate: instead of hand-building a
message list, we fill in a reusable template with a "question" variable,
then pass the resulting messages to the chat model and print its reply.
This shows how to parameterize prompts so the same template can be reused
with different inputs.
"""

# Import the configured chat model and the reusable prompt template.
from model import model
from prompt import prompt

# Fill in the template's {question} placeholder to build the actual
# message list that will be sent to the model.
messages = prompt.invoke(
    {
        "question": "What is an autonomous AI agent?"
    }
)

# Send the rendered messages to the model and get a response back.
response = model.invoke(messages)

# The actual generated text lives in the response's .content attribute.
print(response.content)

