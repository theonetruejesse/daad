"""
    Watch for file changes and restart the script. Nodemon style workflow.
"""

import hashlib
import os
import signal
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, script_to_run):
        self.script_to_run = script_to_run
        self.process = None
        self.last_hash = None
        self.start_script()

    def get_file_hash(self, filepath):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def start_script(self):
        if self.process:
            os.kill(self.process.pid, signal.SIGTERM)
        self.process = subprocess.Popen(["python", self.script_to_run])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            current_hash = self.get_file_hash(event.src_path)
            if current_hash != self.last_hash:
                print(f"{event.src_path} has changed. Restarting script...")
                self.last_hash = current_hash
                self.start_script()


def run():
    script_to_run = "src/daad/main.py"  # Updated path to main script
    path_to_watch = "."  # Watch the current directory

    event_handler = FileChangeHandler(script_to_run)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    run()
