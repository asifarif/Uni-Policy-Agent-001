# app.py – Entry point for Hugging Face Spaces
from app.main import app  # Import the FastAPI app object
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)  # Run FastAPI app on port 7860
