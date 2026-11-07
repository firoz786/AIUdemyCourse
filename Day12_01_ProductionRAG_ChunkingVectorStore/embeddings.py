from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


MODEL = "nomic-embed-text"


def create_embedding(text):

    response = client.embeddings.create(
        model=MODEL,
        input=text
    )

    return response.data[0].embedding


def embed_chunks(chunks):

    embedded_chunks = []

    for chunk in chunks:

        embedding = create_embedding(
            chunk["text"]
        )

        embedded_chunks.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "embedding": embedding
        })

    return embedded_chunks

