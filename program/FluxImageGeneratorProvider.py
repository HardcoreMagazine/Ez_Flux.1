import torch
from program.FluxConfigurationProvider import FluxConfigurationProvider
from program.config.common_image_presets import common_presets

class FluxImageGeneratorProvider():
    pipeline: any
    __torch_generator: torch.Generator
    
    def __init__(self, pipeline: any) -> None:
        self.pipeline = pipeline
        self.__torch_generator = torch.Generator(device="cuda").manual_seed(0) # do not touch this unless you know what are you doing     
    
    def generate_image(self, prompt: str, conf: FluxConfigurationProvider):
        conf.max_seq_len = len(prompt) # I see no easy way to set this otherwise
        
        image = self.pipeline(
            prompt = prompt,
            height = common_presets[conf.img_aspect_ratio][conf.img_size]['h'],
            width = common_presets[conf.img_aspect_ratio][conf.img_size]['w'],
            guidance_scale = conf.scale, 
            num_inference_steps = conf.steps, 
            max_sequence_length = conf.max_seq_len, 
            generator = self.__torch_generator
        ).images[0]
        
        return image