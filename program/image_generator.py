import torch
import pathlib
from configparser import ConfigParser
from program.pipeline_provider import download_model_and_create_pipeline, create_pipeline
from program.pipeline_configurator import configure_pipeline_optimized, configure_pipeline_default
from program.config.common_image_formats import res_presets
from program.utility.filename_generator import get_next_filename
from program.utility.prompt_archiver import log_call_to_file


class ImgGenerator():
    __pipe: any
    __cfg: ConfigParser
    
    # Note that all values described below this line are based on Flux.1.dev model tests
    __scale: float
    """
    Lower values mean more creative image output: 
    when <= 0 - take random, unrealted to prompt base images; 
    when = 1~8 - take random, but related to prompt base images (creative); 
    when >= 9 - take highly related to prompt base images (less creative).
    """
    
    __steps: int
    """
    Higher values mean more image details and longer image generation time: 
    when <5: blurry images; 
    when >=10: simple images;
    when >=20: simple images with blurry background;
    when =50: complex images
    """
    
    __max_seq_len: int
    """
    Maximum prompt length (number of tokens), higher values cause long generation times, 
    but also allow to describe more detail - best keep this to len(prompt) [default]
    """
    
    __img_aspect_ratio: str
    __img_size: str
    __generator: torch.Generator

    __sys_prefix = 'Ez_Flux.1 >>'
    __usr_prefix = 'Ez_Flux.1 <<'

    __proj_dir: str = str(pathlib.Path().resolve())
    __proj_out_img: str = f'{__proj_dir}\\output\\images\\'
    __proj_out_log: str = f'{__proj_dir}\\output\\history\\'
    
    
    def __init__(self, configuration: ConfigParser, model: str, online: bool, auth_token: str = None):
        self.__cfg = configuration
        if not online:
            self.__pipe = create_pipeline(model)
        else:
            self.__pipe = download_model_and_create_pipeline(model, auth_token)        
        self.configure()
        self.run()
    
    
    def configure(self):
        #self.__pipe = configure_pipeline_default(self.__pipe)
        self.__pipe = configure_pipeline_optimized(self.__pipe)
        
        # Generative settings
        self.__img_aspect_ratio = '9:16'
        self.__img_size = 'sd' # bigger resolutions mean longer image generation times
        
        self.__scale: float = 4 # default = 3.5 @ best keep at 3.5~5
        self.__steps: int = 15  # default = 50 @ best keet at 10~20

        self.__generator = torch.Generator(device="cuda").manual_seed(0) # do not touch this unless you know what are you doing     
        
    
    def run(self):
        while True:
            print(f'{self.__sys_prefix} Enter your prompt or type "exit" to exit the program')
            prompt = input(f'{self.__usr_prefix} ')
            if len(prompt) > 1 and not str.isspace(prompt): 
                
                if prompt.strip().lower() == 'exit':
                    break

                self.__max_seq_len = len(prompt)
                
                image = self.__pipe(
                    prompt=prompt,
                    height=res_presets[self.__img_aspect_ratio][self.__img_size]['h'],
                    width=res_presets[self.__img_aspect_ratio][self.__img_size]['w'],
                    guidance_scale=self.__scale, 
                    num_inference_steps=self.__steps, 
                    max_sequence_length=self.__max_seq_len, 
                    generator=self.__generator
                ).images[0]
                
                next_full_filename = f'{self.__proj_out_img}{get_next_filename(self.__proj_out_img)}'
                
                image.save(next_full_filename)
                print(f'{self.__sys_prefix} Saved result as "{next_full_filename}"')
                
                if self.__cfg.getboolean('settings', 'save_prompt_history'):
                    params = f"scale={self.__scale}, steps={self.__steps}, max_seq_len={self.__max_seq_len}"
                    log_call_to_file(self.__proj_out_log, prompt, params, next_full_filename)
            else:
                print(f'{self.__sys_prefix} Bad input, try again')

