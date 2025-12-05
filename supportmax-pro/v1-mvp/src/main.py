import subprocess
import sys
import time
import os
import signal
import atexit

def main():
    """
    Unified launcher for SupportMax Pro v1 MVP
    Starts both the API (FastAPI) and Frontend (Streamlit).
    """
    print("\033[1;36m🚀 Starting SupportMax Pro v1 MVP System...\033[0m")
    
    # Get python executable (ensures we use the same venv)
    python_exe = sys.executable
    project_root = os.getcwd()
    
    # Define paths
    api_script = "src/api/endpoints.py"
    frontend_script = "src/frontend/streamlit_app.py"
    
    # Environment variables
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(project_root, "src")
    
    processes = []

    def cleanup():
        print("\n\033[1;33m🛑 Shutting down services...\033[0m")
        for p in processes:
            if p.poll() is None:  # If running
                p.terminate()
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    p.kill()
        print("\033[1;32m✅ Shutdown complete.\033[0m")

    # Register cleanup on exit
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda sig, frame: sys.exit(0))

    try:
        # 1. Start API Server
        print(f"\n\033[1;34m📡 Launching API Server ({api_script})...\033[0m")
        # Note: v1 API runs on port 8001 by default in endpoints.py if run directly,
        # but the docker-compose said 8000. Let's check endpoints.py again.
        # It had `uvicorn.run(..., port=8001)`.
        
        # ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        log_file = open("logs/api_service.log", "w")

        api_process = subprocess.Popen(
            [python_exe, api_script],
            cwd=project_root,
            env=env,
            stdout=log_file,
            stderr=subprocess.STDOUT, # Redirect stderr to stdout
            text=True # Ensure text mode if needed, though with file object it handles bytes usually. Actually file opened in text mode 'w' defaults to text.
        )
        processes.append(api_process)
        
        # Wait for API to initialize (basic heuristic)
        print("   Waiting for API to start...")
        time.sleep(3)
        
        if api_process.poll() is not None:
            print("\033[1;31m❌ API failed to start.\033[0m")
            sys.exit(1)

        # 2. Start Frontend
        print(f"\n\033[1;35m🖥️  Launching Frontend ({frontend_script})...\033[0m")
        frontend_process = subprocess.Popen(
            [python_exe, "-m", "streamlit", "run", frontend_script],
            cwd=project_root,
            env=env
        )
        processes.append(frontend_process)
        
        print("\n\033[1;32m✨ System Online! Press Ctrl+C to stop.\033[0m")
        print("   - API: http://localhost:8001")
        print("   - Frontend: http://localhost:8501")
        
        # Wait for frontend to exit (user stops it)
        frontend_process.wait()
        
    except Exception as e:
        print(f"\033[1;31m❌ Error: {e}\033[0m")
        cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()
