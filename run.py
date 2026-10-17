"""
One-command launcher for Expense Tracker.
Runs both the FastAPI backend and React frontend concurrently.

Usage:
    python run.py
"""
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

# Safe encoding for Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Checks if a given port is already occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def main():
    print("=" * 60)
    print(">> Starting Expense Tracker (FastAPI + React Dashboard)...")
    print("=" * 60)

    # 1. Port checks & Backend launch
    backend_proc = None
    if is_port_in_use(8000):
        print(" [INFO] Backend port 8000 is already active (using running instance).")
    else:
        print(" [*] Starting FastAPI backend on http://127.0.0.1:8000 ...")
        backend_proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
                "--reload",
            ],
            cwd=str(ROOT_DIR),
        )

    # Wait for backend to be ready
    for _ in range(12):
        if is_port_in_use(8000):
            print(" [OK] Backend is LIVE at: http://127.0.0.1:8000 (Docs: /docs)")
            break
        time.sleep(0.5)
    else:
        print(" [!] Backend starting took longer than expected, proceeding with frontend...")

    # 2. Frontend launch
    frontend_proc = None
    if is_port_in_use(5173):
        print(" [INFO] Frontend port 5173 is already active (using running instance).")
    else:
        print(" [*] Starting React Frontend on http://localhost:5173 ...")
        frontend_proc = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=str(FRONTEND_DIR),
            shell=True,
        )

    print("=" * 60)
    print(" [READY] Both servers are up!")
    print("         • Frontend UI: http://localhost:5173")
    print("         • Backend API: http://127.0.0.1:8000/docs")
    print(" Press Ctrl+C in this terminal anytime to stop.")
    print("=" * 60)

    try:
        while True:
            # Check if backend crashed
            if backend_proc and backend_proc.poll() is not None:
                print("\n[!] Backend process exited.")
                break
            # Check if frontend crashed
            if frontend_proc and frontend_proc.poll() is not None:
                print("\n[!] Frontend process exited.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down servers...")
    finally:
        if backend_proc and backend_proc.poll() is None:
            backend_proc.terminate()
        if frontend_proc and frontend_proc.poll() is None:
            if sys.platform == "win32":
                subprocess.call(
                    ["taskkill", "/F", "/T", "/PID", str(frontend_proc.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                frontend_proc.terminate()
        print("[OK] All servers stopped cleanly.")


if __name__ == "__main__":
    main()
