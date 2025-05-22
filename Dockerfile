# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose FastAPI default port
EXPOSE 7860

# Start FastAPI app
CMD ["python", "start_with_index.py"]
