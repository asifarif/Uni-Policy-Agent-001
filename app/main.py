# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from app.qa_engine import create_qa_chain
from app.vector_store import load_vectorstore, build_vectorstore_if_needed
from fastapi.staticfiles import StaticFiles
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rebuild vectorstore if missing
build_vectorstore_if_needed()

# Initialize FastAPI app
app = FastAPI()

# Load vectorstore and QA chain
vectorstore = load_vectorstore()
qa_chain = create_qa_chain(vectorstore)

@app.post("/query")
async def query_api(request: Request):
    data = await request.json()
    question = data.get("question")

    if not question:
        return JSONResponse(status_code=400, content={"error": "Question is required."})

    try:
        result = qa_chain.invoke({"question": question})
        return {
            "answer": result.get("answer"),
            "sources": result.get("source_documents", [])
        }
    except Exception as e:
        logger.error(f"Error in QA engine: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# Mount static files if available
if os.path.isdir("public"):
    app.mount("/", StaticFiles(directory="public", html=True), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>SSUET Agent 003</title>
        </head>
        <body>
            <h2>🤖 SSUET AI Chatbot is running!</h2>
            <p>Use the <code>/query</code> endpoint to interact with the QA system.</p>
        </body>
    </html>
    """

# uvicorn app.main:app --reload --port 8010