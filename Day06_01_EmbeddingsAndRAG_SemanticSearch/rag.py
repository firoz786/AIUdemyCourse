"""
Day06_01_EmbeddingsAndRAG_SemanticSearch: a simple Retrieval-Augmented
Generation (RAG) chatbot. Instead of relying on the LLM's own knowledge, it
first converts every document in `knowledge/` and the user's question into
embeddings (numeric vectors capturing meaning), finds the single most
similar document using cosine similarity, and then asks the LLM to answer
using only that document as context. This demonstrates the core RAG pattern:
embed -> retrieve the most relevant text -> answer grounded in that text.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
from retriever import load_documents

from test_embedding import create_embedding

from similarity import cosine_similarity

# Load every document from the knowledge folder (filename -> text content).
documents = load_documents()

# Pre-compute an embedding (vector representation) for each document so we
# only have to do this once, not on every question.
document_embeddings = {}

for filename, content in documents.items():

    document_embeddings[filename] = create_embedding(
        content
    )

# Load configuration (BASE_URL, API_KEY, MODEL) from the local .env file.
load_dotenv()

# Create the AI client used to talk to the LLM server.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Simple banner so the user knows the chatbot is ready.
print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

# Main chat loop: keep asking the user for input until they quit.
while True:

    # Ask the user to type a message. Handle Ctrl+C / Ctrl+D gracefully so
    # the program exits cleanly instead of crashing with a traceback.
    try:
        user_input = input("\nYou : ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        break

    # Let the user end the conversation by typing "quit".
    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    # Turn the user's question into an embedding so we can compare its
    # meaning against each document's embedding.
    question_embedding = create_embedding(
    user_input)

    best_score = -1

    best_document = None

    # Find the document whose embedding is most similar (closest meaning)
    # to the question's embedding - this is the "retrieval" step of RAG.
    for filename, embedding in document_embeddings.items():

        score = cosine_similarity(
        question_embedding,
        embedding
        )

        if score > best_score:

            best_score = score

            best_document = filename

    # Use the best-matching document's full text as grounding context.
    context = documents[best_document]

    # Build a prompt that instructs the model to answer using ONLY the
    # retrieved context, instead of its own general knowledge.
    prompt = f"""
Answer the question using only
the following information.

Context:

{context}

Question:

{user_input}
"""

    # Ask the model to answer, grounded in the retrieved document.
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nAI :", response.choices[0].message.content)

