import pytest
import subprocess
import time
import sys
import os
import signal
import requests

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

# Global variable to store server process
server_process = None


@pytest.fixture(scope="session", autouse=True)
def flask_server():
    """Start Flask server before tests and stop it after."""
    global server_process

    # Path to app.py
    app_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'backend',
        'app.py'
    )

    print("\n" + "="*60)
    print("Starting Flask server for testing...")
    print("="*60)

    # Start Flask server in background
    server_process = subprocess.Popen(
        [sys.executable, app_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for server to be ready (check if it responds)
    max_retries = 10
    for i in range(max_retries):
        time.sleep(1)

        # Check if server process is still running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            print(f"Server failed to start!\nSTDOUT: {stdout}\nSTDERR: {stderr}")
            pytest.exit("Flask server failed to start")

        # Try to connect to the server
        try:
            response = requests.get("http://localhost:5001/", timeout=1)
            if response.status_code == 200:
                print(f"Flask server is ready (attempt {i+1}/{max_retries})")
                break
        except (requests.ConnectionError, requests.Timeout):
            print(f"Waiting for server... (attempt {i+1}/{max_retries})")
            continue
    else:
        pytest.exit("Flask server failed to respond within timeout")

    print("Flask server started successfully")
    print("="*60)

    yield

    # Cleanup: Stop server after all tests
    print("\n" + "="*60)
    print("Stopping Flask server...")
    print("="*60)

    if server_process:
        # Terminate the process
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

    print("Flask server stopped")


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application."""
    return "http://localhost:5001"
