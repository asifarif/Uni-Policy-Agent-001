# app/data_loader.py
#This module is responsible for:
#Downloading university policy PDFs from Google Drive (via file IDs).
#Extracting structured text and tables using pdfplumber.
#Returning them as LangChain Document objects for vector storage.


import json
import requests
import pdfplumber
import io
from langchain.docstore.document import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Downloads a file by its Google Drive ID, handling the confirmation page for large files.
def download_pdf_from_google_drive(file_id: str) -> bytes:
    """Downloads a PDF from Google Drive by file ID and returns bytes."""
    try:
        URL = "https://drive.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params={"id": file_id}, stream=True)

        # Handle large file warning (Google drive download guard)
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                response = session.get(URL, params={"id": file_id, "confirm": value}, stream=True)
                break

        if response.status_code == 200:
            return response.content
        else:
            logger.error(f"Failed to download file {file_id}: Status {response.status_code}")
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {str(e)}")

    return None

# Uses pdfplumber to extract text and tables from each page.
# Combines content, ignores pages with <50 characters.
# Packages each page as a Document with metadata.
def extract_text_from_pdf(pdf_bytes: bytes, metadata: dict) -> list:
    """Extracts text and tables from a PDF and returns LangChain Document list."""
    documents = []
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                tables = page.find_tables()
                table_text = ""

                for table in tables:
                    extracted = table.extract()
                    if extracted:
                        table_text += "\n".join([
                            " | ".join(cell or "" for cell in row)
                            for row in extracted if any(row)
                        ]) + "\n"

                combined = f"{text}\n{table_text}".strip()

                if len(combined) >= 50:
                    documents.append(Document(
                        page_content=combined,
                        metadata={**metadata, "page": i + 1, "source": f"{metadata.get('title', 'Untitled')} - Page {i + 1}"}

                    ))
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")

    return documents

# Loads your policy_links.json.
# Loops through the list, downloads PDFs, extracts data, and returns a list of Documents.
def load_policy_documents(json_path="policy_links.json") -> list:
    """Main function to load all university policies from JSON config."""
    documents = []
    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        for item in data.get("policies", []):
            title = item.get("title")
            file_id = item.get("gdrive_id")

            if not title or not file_id:
                logger.warning(f"Skipping invalid entry: {item}")
                continue

            pdf_bytes = download_pdf_from_google_drive(file_id)
            if not pdf_bytes:
                continue

            docs = extract_text_from_pdf(pdf_bytes, metadata={
                "title": title,
                "approval_date": item.get("approval_date", "Unknown"),
                "policy_number": item.get("policy_number", "N/A"),
                "source": f"https://drive.google.com/file/d/{file_id}/view" 

            })
            documents.extend(docs)

    except Exception as e:
        logger.error(f"Failed to load policy JSON: {str(e)}")

    return documents
