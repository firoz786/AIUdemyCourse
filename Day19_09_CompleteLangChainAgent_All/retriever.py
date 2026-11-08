"""
Day 19.09 - Building the RAG retriever (vector store setup).

This module builds the semantic-search "retriever" shared by the other
scripts: it loads notes.txt, splits it into overlapping text chunks,
turns each chunk into an embedding vector (via Ollama's nomic-embed-text
model), stores those vectors in an in-memory FAISS index, and exposes a
`retriever` object that other files use to find the most relevant chunks
for a given question.
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


# Load the raw text of notes.txt as a single LangChain Document.
loader = TextLoader(
    "notes.txt",
    encoding="utf-8"
)

documents = loader.load()

# Split the document into smaller overlapping chunks so the retriever can
# return focused snippets instead of the whole file.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

# Convert text chunks into numeric embedding vectors using a local
# Ollama embedding model.
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Build an in-memory FAISS vector store/index from the chunk embeddings.
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

# Expose a retriever: given a query, it returns the most similar chunks.
retriever = vector_store.as_retriever()
