# -------- Stage 1: Build dependencies --------
FROM python:3.10-slim AS builder

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install packages into a virtual location
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# -------- Stage 2: Final runtime image --------
FROM python:3.10-slim

# Create non-root user (required by Hugging Face)
RUN useradd -m -u 1000 user
USER user

WORKDIR /home/user/app

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy app source code
COPY --chown=user . .

# Set default environment variables
ENV PORT=7860
ENV CMD_EXEC="python start_with_index.py"

EXPOSE $PORT

# Run the command based on CMD_EXEC
CMD bash -c "$CMD_EXEC"
