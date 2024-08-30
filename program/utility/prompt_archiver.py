import os
from datetime import datetime

def log_call_to_file(archive_path: str, prompt: str, params: str, filename: str):
    """
    Saves given prompt, params, filename and datetime stamp in "./output/history/prompt_history.txt" for future references.
    """
    
    # Set the working directory to "./history" project subfolder
    os.chdir(archive_path)
    # Open or create a text file named 'prompt_history.txt' in append mode
    with open('prompt_history.txt', 'a') as f:
        #Write your string variable to the end of the file with a new line
        f.write(f"[{datetime.now()}] prompt: \"{prompt}\" @ params: {params} @ filename: {filename}\n")
        f.close()