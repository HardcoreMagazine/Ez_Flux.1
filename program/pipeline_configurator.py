import torch


def configure_pipeline_optimized(pipe):
    pipe.enable_model_cpu_offload() # save some VRAM by offloading the model to CPU. Comment this if you have enough GPU power
    pipe.enable_sequential_cpu_offload()
    pipe.vae.enable_slicing()
    pipe.vae.enable_tiling()
    pipe.to(torch.float32) # casting here instead of in the pipeline constructor because doing so in the constructor loads all models into CPU memory at once
    return pipe

def configure_pipeline_default(pipe):
    pipe.to(torch.float32)
    return pipe