import subprocess
import time
import requests
import signal
import sys
import platform

# Import test modules
import test.test_loader as test_loader
import test.test_vector_store as test_vector_store
import test.test_qa_engine as test_qa_engine
import test.test_main_api as test_main_api

def wait_for_server(url: str, timeout: int = 15):
    """Wait for the server to start responding."""
    print(f"Waiting for server at {url}...")
    for _ in range(timeout):
        try:
            response = requests.get(url)
            if response.status_code in (200, 404):
                print("✅ Server is up!")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    raise TimeoutError(f"Server at {url} did not become ready in time.")

def run_tests():
    print("\n🧪 Running test_loader.py...")
    test_loader.test_load_documents()
    time.sleep(1)

    print("\n🧪 Running test_vector_store.py...")
    test_vector_store.test_vector_store()
    time.sleep(1)

    print("\n🧪 Running test_qa_engine.py...")
    test_qa_engine.test_qa_engine()
    time.sleep(1)

    print("\n🚀 Starting FastAPI server...")
    server = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        wait_for_server("http://127.0.0.1:8000")

        print("\n🧪 Running test_main_api.py...")
        test_main_api.test_query()
        time.sleep(1)

    finally:
        print("\n🛑 Stopping server...")
        if platform.system() == "Windows":
            server.terminate()
        else:
            server.send_signal(signal.SIGINT)
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
        print("✅ Server stopped.")

if __name__ == "__main__":
    run_tests()



