from app.data_loader import load_policy_documents

def test_load_documents():
    docs = load_policy_documents("policy_links.json")

    # Basic sanity checks
    assert isinstance(docs, list), "Expected result to be a list"
    assert all(hasattr(doc, "page_content") for doc in docs), "Each doc should have 'page_content'"
    assert all(hasattr(doc, "metadata") for doc in docs), "Each doc should have 'metadata'"
    
    # Optional: Print summary
    print(f"✅ Loaded {len(docs)} documents.")
    if docs:
        print("📄 Sample document:")
        print(docs[0].page_content[:300])

if __name__ == "__main__":
    test_load_documents()
