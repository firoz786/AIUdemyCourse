"""
Day 19.08 - Memory with LangChain (Conversation).

This script is the RAG (Retrieval-Augmented Generation) demo carried over
from Day 19.07. It builds a small chain that: (1) takes a question, (2)
retrieves relevant chunks of text from our vector store (via retriever.py),
(3) stuffs those chunks into a prompt as "context", and (4) asks the chat
model to answer using only that context. It then runs the chain once on a
sample question and prints the answer.
"""

from model import model  # The chat model that will generate the final answer.
from retriever import retriever  # Vector-store-backed retriever that finds relevant notes.

from langchain_core.prompts import ChatPromptTemplate  # Builds the prompt that combines context + question.
from langchain_core.output_parsers import StrOutputParser  # Converts the model's message output into a plain string.


# Prompt template: instructs the model to answer only from the given context.
prompt = ChatPromptTemplate.from_template(
    """
Answer the question using only the provided context.

Context:
{context}

Question:
{question}
"""
)


def get_context(question):
    # Use the retriever to fetch the most relevant document chunks for this question.
    documents = retriever.invoke(question)

    # Join all retrieved chunks into one text block, separated by blank lines.
    return "\n\n".join(
        document.page_content
        for document in documents
    )


# Build the RAG pipeline: fill in context + question, format the prompt,
# send it to the model, then parse the model's reply into plain text.
chain = (
    {
        "context": get_context,
        "question": lambda x: x
    }
    | prompt
    | model
    | StrOutputParser()
)


# Run the chain end-to-end with a sample question and print the answer.
answer = chain.invoke(
    "What is MCP?"
)

print(answer)

