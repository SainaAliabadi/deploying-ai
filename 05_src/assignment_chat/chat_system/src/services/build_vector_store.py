import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from chat_system.src.config import settings


def build_vector_store():
    # Load raw text
    with open("chat_system/knowledge_base.txt", "r") as f:
        text = f.read()

    # Split into chunks (simple split)
    chunks = [chunk.strip() for chunk in text.split("\n") if chunk.strip()]

    documents = [Document(page_content=chunk) for chunk in chunks]

    embeddings = OpenAIEmbeddings()

    vector_store = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=settings.CHROMA_DIR,
        collection_name=settings.COLLECTION_NAME
    )

    vector_store.persist()
    print("✅ Vector store built and persisted.")
