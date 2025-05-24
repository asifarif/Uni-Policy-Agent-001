# app/qa_engine.py

import os
import logging
from typing import Optional
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain_core.language_models.llms import LLM
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.vector_store import load_vectorstore
import requests
from langchain.chains import RetrievalQAWithSourcesChain


# Logging config
logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "DeepSeek-R1-Distill-Qwen-32B"
# MODEL_NAME = "mixtral-8x7b-32768"
# MODEL_NAME = "deepseek-r1-distill-llama-70b"

class GroqLLM(LLM):
    """Custom LangChain-compatible wrapper for Groq API."""

    model: str = MODEL_NAME
    temperature: float = 0.25
    max_tokens: int =  512 # need to check the impact of max_tokens
    api_key: Optional[str] = GROQ_API_KEY

    @property
    def _llm_type(self) -> str:
        return "groq"

    def _call(self, prompt: str, stop: Optional[list[str]] = None) -> str:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set.")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Groq API error: {response.status_code} {response.text}")

        return response.json()["choices"][0]["message"]["content"].strip()


def create_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever()
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=GroqLLM(model=MODEL_NAME, api_key=os.getenv("GROQ_API_KEY")),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    return chain
