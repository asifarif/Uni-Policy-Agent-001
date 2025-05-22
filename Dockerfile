# -------- Stage 1: Build dependencies --------
FROM python:3.10-slim AS builder

WORKDIR /app

# System dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install packages into a virtual location
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# -------- Stage 2: Final runtime image --------
FROM python:3.10-slim

WORKDIR /app

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy app source
COPY . .

# Expose FastAPI/Gradio/etc. port
EXPOSE 7860

# Default command to run app
CMD ["python", "start_with_index.py"]
