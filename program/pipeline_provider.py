import torch
from diffusers import FluxPipeline
from huggingface_hub import login

def download_model_and_create_pipeline(full_model_name: str, auth_token: str = None):
    if auth_token and len(auth_token) > 0:
        login(token=auth_token)
    #pipe = FluxPipeline.from_pretrained(full_model_name, torch_dtype=torch.bfloat16, cache_dir=cfg["download_path"])
    pipe = FluxPipeline.from_pretrained(full_model_name, torch_dtype=torch.bfloat16)
    return pipe


def create_pipeline(full_model_path: str):
    pipe = FluxPipeline.from_pretrained(full_model_path, torch_dtype=torch.bfloat16)
    return pipe
