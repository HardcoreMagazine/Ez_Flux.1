import pathlib

def get_next_filename(out_img_dir: str) -> str:
    """
    Returns the next available filename based on the current file count.
    
    Args:
        img_output_dir (str): The path to the 'images' folder.
        
    Returns:
        str: The next available filename in the format of "N.png" where N is an integer.
    """

    # Get a list of all files in the directory
    image_files = [f for f in pathlib.Path(out_img_dir).glob('*.png')]
    
    if not image_files:
        return "1.png"
    
    max_id = max(int(f.stem) for f in image_files)
    next_filename = str(max_id + 1) + ".png"
    
    return next_filename
