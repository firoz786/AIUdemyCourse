"""
Day 19.09 - Retrieval-Augmented Generation (RAG) chain example.

This script demonstrates a classic RAG pipeline using LangChain's "pipe"
(`|`) syntax: it retrieves relevant chunks from notes.txt (via the shared
`retriever`), stuffs them into a prompt as "context" alongside the user's
question, sends that prompt to the LLM, and parses the response into a
plain string. Running the file directly asks "What is MCP?" and prints
the model's grounded answer.
"""

from model import model
from retriever import retriever

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Prompt template: the model must answer using ONLY the retrieved context,
# which helps reduce hallucination (making things up).
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
    # Retrieve the most relevant chunks from the vector store for this question.
    documents = retriever.invoke(question)

    # Join the chunks into one text block to inject into the prompt.
    return "\n\n".join(
        document.page_content
        for document in documents
    )


# Build the RAG chain: compute "context" and pass through "question",
# feed both into the prompt, send the prompt to the model, then parse
# the model's reply into a plain Python string.
chain = (
    {
        "context": get_context,
        "question": lambda x: x
    }
    | prompt
    | model
    | StrOutputParser()
)


# Run the chain once with a sample question and print the answer.
answer = chain.invoke(
    "What is MCP?"
)

print(answer)

