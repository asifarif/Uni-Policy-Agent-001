# test/test_qa_engine.py

from app.qa_engine import create_qa_chain
from app.vector_store import load_vectorstore

def test_qa_engine():
    # Load the FAISS vectorstore
    vectorstore = load_vectorstore()

    # Create the QA chain
    qa_chain = create_qa_chain(vectorstore)

    # Example query
    query = "What is the university's attendance policy?"
    result = qa_chain.invoke({"question": query})  # Make sure input is a dict

    print("Query:", query)
    print("Answer:", result['answer'])  # Use 'answer' for RetrievalQAWithSourcesChain

    print("\nSources:")
    for doc in result['source_documents']:
        print(f"- Title: {doc.metadata.get('title')} | Page: {doc.metadata.get('page')}")

if __name__ == "__main__":
    test_qa_engine()
