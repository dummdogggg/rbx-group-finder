import threading
import subprocess
import time

# Set a limit for the number of threads to prevent system overload
MAX_THREADS = 2000
threads = []

def run_script():
    # Run main.py in a subprocess
    subprocess.run(["python", "main.py"])

while True:
    # Clean up finished threads
    threads = [t for t in threads if t.is_alive()]

    # Start a new thread if below the limit
    if len(threads) < MAX_THREADS:
        thread = threading.Thread(target=run_script)
        thread.start()
        threads.append(thread)

    # Small delay to prevent excessive CPU usage
    time.sleep(1)
