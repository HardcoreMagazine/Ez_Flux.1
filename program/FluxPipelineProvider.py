import torch
from diffusers import FluxPipeline
from huggingface_hub import login

class FluxPipelineProvider():
    pipeline: any
    
    
    def __init__(self, model_path: str, online_mode: bool = False, use_optimized_settings: bool = True, auth_token: str = None) -> None:
        if online_mode:
            self.__download_model_and_create_pipeline(model_path, auth_token)
        else:
            self.__load_model_and_create_pipeline(model_path)
        
        if use_optimized_settings:
            self.__configure_pipeline_ram_optimized()
        else:
            self.__configure_pipeline_default()
    
    
    def __download_model_and_create_pipeline(self, full_model_name: str, auth_token: str = None) -> None:
        if auth_token and len(auth_token) > 0:
            login(token = auth_token)
        self.pipeline = FluxPipeline.from_pretrained(full_model_name, torch_dtype=torch.bfloat16)


    def __load_model_and_create_pipeline(self, full_model_path: str) -> None:
        self.pipeline = FluxPipeline.from_pretrained(full_model_path, torch_dtype=torch.bfloat16)


    def __configure_pipeline_ram_optimized(self) -> None:
        """
        This method configures pipeline in a way that it would use RAM instead of VRAM 
        while also sharing generation process load between CPU and GPU
        """
        
        self.pipeline.enable_model_cpu_offload() # save some VRAM by offloading the model to CPU. Comment this if you have enough GPU power
        self.pipeline.enable_sequential_cpu_offload()
        self.pipeline.vae.enable_slicing()
        self.pipeline.vae.enable_tiling()
        self.pipeline.to(torch.float32) # casting here instead of in the pipeline constructor because doing so in the constructor loads all models into CPU memory at once


    def __configure_pipeline_default(self) -> None:
        self.pipeline.to(torch.float16)

