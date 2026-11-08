"""
Day 20.06 - Production Complete Agent API.

Builds the local knowledge base used by the RAG tool. It loads notes.txt,
splits it into overlapping chunks, embeds those chunks with an Ollama
embedding model, and stores the resulting vectors in an in-memory FAISS
index so they can be searched by semantic similarity at query time.
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Load the raw knowledge base text file as a single LangChain Document.
loader = TextLoader(
    "notes.txt",
    encoding="utf-8"
)

documents = loader.load()

# Break the document into overlapping chunks so retrieval returns focused,
# bite-sized pieces of context instead of the whole file.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

# Embedding model that turns each text chunk into a numeric vector capturing
# its meaning, so similar chunks end up close together in vector space.
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Build an in-memory vector index from the embedded chunks.
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

# Expose a retriever interface: given a query, it returns the most
# semantically similar chunks from the vector store.
retriever = vector_store.as_retriever()
