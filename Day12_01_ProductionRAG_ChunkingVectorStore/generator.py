"""
Day12 - Production RAG: Chunking & Vector Store
=================================================
This module is the "Generation" half of RAG: it takes the chunks
retrieved from the vector store and asks a local LLM (via Ollama) to
write a final answer grounded only in that retrieved context. Keeping
the model restricted to the provided context (instead of its own
training data) is what makes RAG answers more trustworthy and
traceable back to the source documents.
"""
from openai import OpenAI

# Reuse the same local Ollama server as the embeddings module, but talk
# to the chat/completions endpoint instead of the embeddings endpoint.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# The chat model used to generate the final answer.
MODEL = "qwen3:1.7b"


def generate_answer(query, results):
    """Ask the LLM to answer `query` using only the retrieved `results`."""
    # Join all retrieved chunk texts into one block of context text.
    context = "\n\n".join(result["text"] for result in results)

    # The prompt explicitly tells the model to stick to the given
    # context and admit when the answer isn't present.
    prompt = f"""
Answer the user's question using
only the provided context.

Context:
{context}

Question:
{query}

Rules:

1. Use only the provided context.
2. Do not invent information.
3. If the answer is not present,
   say that the information is
   not available.
4. Give a clear and concise answer.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract the plain text answer from the chat completion response.
    return response.choices[0].message.content.strip()

