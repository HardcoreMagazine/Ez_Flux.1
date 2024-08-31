import os
from datetime import datetime

def log_call_to_file(archive_path: str, prompt: str, params: str, filename: str) -> None:
    """
    Logs datetime stamp, prompt, call parameters and filename to "**archive_path**\\prompt_history.txt".
    """
    
    # Set the working directory
    os.chdir(archive_path)
    # Open or create a text file named 'prompt_history.txt' in append mode
    with open('prompt_history.txt', 'a') as f:
        f.write(f"[{datetime.now()}] prompt: \"{prompt}\" @ params: {params} @ filename: {filename}\n")
        f.close()