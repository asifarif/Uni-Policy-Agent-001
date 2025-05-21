# test/test_vector_store.py
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data_loader import load_policy_documents
from app.vector_store import build_vectorstore, load_vectorstore

def test_vector_store():
    docs = load_policy_documents("policy_links.json")
    print(f"Loaded {len(docs)} documents")

    # Build vector store
    vs = build_vectorstore(docs)
    print("Vector store built and saved.")

    # Load it back
    loaded_vs = load_vectorstore()
    print("Vector store loaded.")

    # Simple similarity test
    result = loaded_vs.similarity_search("graduation requirements", k=1)
    print("Top result content snippet:\n", result[0].page_content[:200])

if __name__ == "__main__":
    test_vector_store()
