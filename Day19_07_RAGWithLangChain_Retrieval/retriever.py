"""
Day 19.07 - RAG with LangChain (Retrieval).

This module builds the retrieval piece of the RAG pipeline. It loads the
text notes from notes.txt, splits them into small overlapping chunks,
turns each chunk into a vector embedding, stores those vectors in an
in-memory FAISS index, and exposes a `retriever` object that other scripts
(rag.py, test_retriever.py) can use to fetch relevant chunks for a query.
"""

from langchain_community.document_loaders import TextLoader  # Reads a plain text file into LangChain Document objects.
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Splits long text into smaller overlapping chunks.
from langchain_ollama import OllamaEmbeddings  # Turns text chunks into numeric vector embeddings via Ollama.
from langchain_community.vectorstores import FAISS  # In-memory vector database for fast similarity search.


# Load the raw notes file as a single LangChain Document.
loader = TextLoader(
    "notes.txt",
    encoding="utf-8"
)

documents = loader.load()

# Break the document into smaller chunks (300 chars, 50 overlap) so retrieval
# can return focused, relevant pieces of text rather than the whole file.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

# Model used to convert each text chunk into a vector embedding.
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Build the FAISS vector store from the chunks and their embeddings.
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

# Expose a retriever interface: given a query, it returns the most similar chunks.
retriever = vector_store.as_retriever()
