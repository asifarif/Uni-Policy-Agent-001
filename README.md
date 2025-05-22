---
title: SSUET AnswerHub
emoji: 🌍
colorFrom: blue
colorTo: indigo
sdk: static  # Use 'static' for FastAPI with static files
app_file: app.py
app_port: 7860
python_version: 3.10
pinned: false
license: mit
short_description: 'SSUET AI-powered policies assistant'
dependencies:
  - fastapi
  - uvicorn
  - sentence-transformers
  - langchain
  - openai
  - tiktoken
  - faiss-cpu
  - pdfplumber
  - pypdf
  - requests
  - python-dotenv
  - huggingface-hub
  - pandas
  - tqdm
---
"# Uni-Policy-Agent-001"

# 🧠 Uni-Policy-Agent
A conversational AI assistant designed to help users understand university policies using LLMs, document indexing, and vector search.
---
## 📁 Project Structure
├── .env # Environment variables (do NOT commit)
├── Dockerfile # Multi-stage Docker build
├── docker-compose.yml # Service configuration
├── policy_links.json # Source links to university policies
├── vectorstore_index/ # Vector DB index (mounted at runtime)
├── requirements.txt # Python dependencies
├── start_with_index.py # App entry point
└── ...


---
## 🚀 Features

- Uses LangChain + FAISS or similar vector DBs for semantic search
- Indexed university policy documents
- Dockerized & deployable via GitHub Actions
- CI/CD to Hugging Face Spaces or custom cloud via Docker Registry
- Gradio / FastAPI frontend
- Works locally or via Docker

---
## 🛠️ Requirements

- Python 3.10+
- Docker Desktop installed and running
- GitHub account
- Hugging Face account (for deployment)
- DockerHub account (optional for registry)

---

## 📦 Installation (Local Development)
### 1. Clone the repo

```bash
git clone https://github.com/asifarif/Uni-Policy-Agent.git
cd Uni-Policy-Agent

2. Create .env file
# .env
OPENAI_API_KEY=your_openai_key_here
HF_TOKEN=your_huggingface_token

3. Install dependencies (optional virtualenv)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

4.Running Tests 
To check each module is working run:
python run_tests.py 

5. Run Locally (Without Docker)
python start_with_index.py
Access the app at: http://localhost:7860

🐳 Docker Workflow
🧱 Build Docker Image
docker build -t uni-policy-agent:v1 .
▶️ Run Docker Image

docker run --env-file .env -p 7860:7860 \
  -v $(pwd)/policy_links.json:/app/policy_links.json \
  -v $(pwd)/vectorstore_index:/app/vectorstore_index \
  uni-policy-agent:v1

🧩 Or Use Docker Compose
docker compose up --build
Make sure Docker context is set to desktop-linux:

docker context use desktop-linux
📦 Pushing Image to DockerHub
Tag your image and push to DockerHub:

docker tag uni-policy-agent:v1 asifarif/uni-policy-agent:v1
docker login
docker push asifarif/uni-policy-agent:v1


🚀 CI/CD Deployment to Hugging Face (via GitHub Actions)
1. Add GitHub Secrets
Go to your GitHub repo → Settings → Secrets → Actions and add:

SSUET_AGENT001 — Hugging Face access token
2. .github/workflows/deploy.yml

name: Deploy to Hugging Face Spaces

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Configure Git
        run: |
          git config --global user.email "asif.arif@gmail.com"
          git config --global user.name "asifarif"

      - name: Deploy to Hugging Face Spaces
        env:
          SSUET_AGENT001: ${{ secrets.SSUET_AGENT001 }}
        run: |
          git remote add space https://huggingface.co/spaces/muasif/SSUET-Agent01
          git push --force https://muasif:${SSUET_AGENT001}@huggingface.co/spaces/muasif/SSUET-Agent01 main

📁 Best Practices
Never commit .env or credentials.
Use docker compose instead of legacy docker-compose (V2+).
Use requirements.txt for Python dependencies and pin versions.
Mount policy_links.json and vectorstore_index as volumes.
Use GitHub Secrets for all tokens (e.g. OpenAI, Hugging Face).
Automate deployment using GitHub Actions and DockerHub/Spaces.

🧯 Troubleshooting
🐳 Cannot connect to Docker daemon?
docker context use desktop-linux
docker compose up
💥 Permissions on .env?
Ensure .env is readable:
chmod 600 .env

🐍 Virtual environment not activating?
Make sure you’re in the right path:

source venv/bin/activate

📤 Future CI/CD (Optional)
Push image to DockerHub automatically
Deploy to AWS (ECS / Lambda / EC2) or Azure App Service
Use a .env.template file to share variable structure
Linting, testing in CI (e.g. flake8, pytest)

🙌 Credits
Developed by Dr. Muhammad Asif
Built with LangChain, Gradio, Hugging Face, and Docker ❤️