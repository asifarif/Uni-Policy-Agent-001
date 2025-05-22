# app/vector_store.py

import os
import logging
import requests
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === NEW: Automatically download remote FAISS index and policy file if missing ===
VECTOR_DIR = "vectorstore_index"
VECTOR_URL = "https://huggingface.co/datasets/muasif/SSUET-POLICY-VECTOR/resolve/main/index.faiss"
POLICY_URL = "https://huggingface.co/datasets/muasif/SSUET-POLICY-VECTOR/resolve/main/policy_links.json"

def download_file_if_missing(url, filepath):
    if not os.path.exists(filepath):
        print(f"⬇️ Downloading {filepath} from {url} ...")
        r = requests.get(url)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"✅ Saved {filepath}")

def prepare_files():
    os.makedirs(VECTOR_DIR, exist_ok=True)
    download_file_if_missing(POLICY_URL, "policy_links.json")
    download_file_if_missing(VECTOR_URL, os.path.join(VECTOR_DIR, "index.faiss"))

prepare_files()
# === End of remote file fetch ===

# Constants
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_DIR = "vectorstore_index"

def get_embedding_model():
    """Initializes the HuggingFace embedding model."""
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        return embeddings
    except Exception as e:
        logger.error(f"Failed to load embedding model: {e}")
        raise

def build_vectorstore(documents: list[Document], persist: bool = True) -> FAISS:
    """Builds and optionally saves a FAISS vectorstore."""
    try:
        for doc in documents:
            if "source" not in doc.metadata:
                doc.metadata["source"] = "unknown"

        embeddings = get_embedding_model()
        vectorstore = FAISS.from_documents(documents, embeddings)

        if persist:
            vectorstore.save_local(INDEX_DIR)
            logger.info(f"FAISS index saved at '{INDEX_DIR}'")

        return vectorstore
    except Exception as e:
        logger.error(f"Failed to build vector store: {e}")
        raise

def load_vectorstore() -> FAISS:
    """Loads an existing FAISS vectorstore from disk."""
    try:
        embeddings = get_embedding_model()
        return FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        logger.error(f"Failed to load FAISS index: {e}")
        raise

def build_vectorstore_if_needed():
    if not os.path.exists("vectorstore_index/index.pkl"):
        from app.data_loader import load_policy_documents

        print("⚙️ No index found. Building vectorstore index...")
        docs = load_policy_documents("policy_links.json")
        build_vectorstore(docs, persist=True)
        print("✅ Vectorstore index created.")
