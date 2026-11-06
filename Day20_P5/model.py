import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama


load_dotenv()


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen3:1.7b"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)


model = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)
