
class FluxConfigurationProvider():
    img_aspect_ratio: str
    """
    Supported image aspect ratios: '1:1', '4:3', '16:9', '9:16'
    """
    
    img_size: str
    """
    Supported image resolutions: 'sd', 'hd', 'fhd', 'uhd', '4k'
    
    Note: from my test runs I found that this parameter ALONG WITH 'steps' directly affects VRAM usage: 
    program has crashed with 16 GB of VRAM on 'schnell' model (with optimized settings) when I tried to use 'fhd' size with steps >= 2 
    """
    
    scale: float # default = 3.5 @ best keep at 3.5~6
    """
    Lower values mean more creative image output: 
    when <= 0 - take random, unrealted to prompt base images; 
    when = 1~8 - take random, but related to prompt base images (creative); 
    when >= 9 - take highly related to prompt base images (less creative).
    """
    
    steps: int # default = 50 @ best keet at 10~20 for faster generation
    """
    Higher values mean more image details and longer image generation time: 
    when <5: blurry images; 
    when >=10: simple images;
    when >=20: simple images with blurry background;
    when >=40: complex images.
    
    Note: 'schnell' model normally only needs 4-10 steps
    """
    
    max_seq_len: int # default = 512 @ best keep this dynamic, 'len(prompt)'
    """
    Maximum prompt length (number of tokens), higher values cause long generation times, 
    but also allow to describe more detail
    """
    
    def __init__(self, img_aspect_ratio: str = '9:16', img_size: str = 'hd', scale: float = 5, steps: int = 10, max_seq_len: int = None) -> None:
        self.img_aspect_ratio = img_aspect_ratio
        self.img_size = img_size
        self.scale = scale
        self.steps = steps
        self.max_seq_len = max_seq_len
    
