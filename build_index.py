# build_index.py

import os
from app.data_loader import load_policy_documents
from app.vector_store import build_vectorstore

INDEX_DIR = "vectorstore_index"

def main(force_rebuild=False):
    if os.path.exists(INDEX_DIR) and not force_rebuild:
        print(f"⚠️ '{INDEX_DIR}/' already exists. Skipping rebuild.")
        return

    print("🔄 Loading documents from policy_links.json...")
    documents = load_policy_documents()

    if not documents:
        print("❌ No documents loaded. Aborting vector store build.")
        return

    print(f"✅ Loaded {len(documents)} documents.")
    print("⚙️ Building and saving vectorstore...")
    build_vectorstore(documents, persist=True)
    print("✅ Vectorstore built and saved to 'vectorstore_index/'.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build FAISS vector store from policy links.")
    parser.add_argument('--force', action='store_true', help="Force rebuild even if index exists.")
    args = parser.parse_args()

    main(force_rebuild=args.force)
