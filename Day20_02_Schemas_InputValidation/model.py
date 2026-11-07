import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama


load_dotenv()


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen3:1.7b"
)


model = ChatOllama(
    model=MODEL_NAME
)
