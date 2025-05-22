# start_with_index.py
import os
import subprocess
import uvicorn

# Check if index exists, otherwise build
if not os.path.exists("vectorstore_index") or not os.listdir("vectorstore_index"):
    print("Building vector index...")
    subprocess.run(["python", "build_index.py", "--force"], check=True)
else:
    print("Vector index found. Skipping build.")

# Start FastAPI
uvicorn.run("app.main:app", host="0.0.0.0", port=7860)
