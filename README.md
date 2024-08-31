# Ez_Flux1.dev
Super-lightweight and easy-to-use terminal shell for Flux.1 image generative model created for people 
who like light-weight solutions with full control over everything happening in the code.

## this README is WIP, some informataion might be outdated as of now

Current state of the project: the program is working as expected; tested on NVIDA RTX 3080 Ti mobile GPU 16 GB + 32GB RAM; additional features 
and better optimization logic is in progress.

## Features 
+ Image generation on demand (obviously)
+ Everythng is customizeable
+ Fully-automatic file name generation system & file saving
+ Fully-automatic call history logging (can be disabled during first launch or inside [settings](/program/config/appsettings.ini))
+ Can be used on machines with borked / outdated GPU driver and on machines with low VRAM (don't expect any miracles though)

## Initial setup (important)
Before you get to play with Flux.1 image generator, the model needs to downloaded on your local hard drive. 
The download process is semi-automatic / guided. 

> Note that the both 'Fast' and 'Dev' models use **30~40 GB** of free disk space by default (each). 

### How to set huggingface access token (for 'Dev' model): 
+ Open [Flux1.dev webpage](https://huggingface.co/black-forest-labs/FLUX.1-dev) in your browser
+ Log in or Sign Up, agree to model access terms
+ Click on your avatar, open Settings page
+ Select Access Tokens and press "Create New Token"
+ In "token type" bar select "Read", add token name and click "Create token"
+ Keep page open for now, you'll need to copy access token later
+ Back in the project: open [config](/program/config/) catalog
+ Open file "user_secrets.md", copy everything inside
+ Create a new file with name: "user_secrets.py" and paste
+ Copy your access token from huggingface webpage and replace value inside marked quotes '...', save and close the file

## How to use
+ Open project folder with VSCode or whichever code editor you're using
+ Run [main.py](main.py) script (I'm using **Python 3.10.6** for package compatibility)
+ Follow the instructions on screen (if any)
+ After successful load of the Flux.1 model you'll be asked to "enter your prompt" - type your desired request. Empty and whitespace-only requests will be automatically handled by the program as invalid. 
+ If you wish to exit the program type "exit" instead of your request - or simply kill the process, should free-up system memory either way.

## Changing model call parameters
Each change in call parameters will require program to be restarted.
+ Open [image_generator.py](/program/image_generator.py) and look for `def configure(self):` line
+ Below this line you'll find 4 most important variables that can be changed:
```
self.__img_aspect_ratio = '9:16'
self.__img_size = 'sd'
self.__scale: float = 4
self.__steps: int = 15
```
+ Descriptions for variables '__scale' and '__steps' provided above, in the same file.
+ Common image aspect ratios and resolutions located in [common_image_formats.py](/program/config/common_image_formats.py) file


## Switching between models
Open [settings](/program/config//appsettings.ini) and set value of "initilized" variable to False, i.e. `initilized = False` and then launch /restart the program. Note that old model will not be deleted this way, in order to switch back you'll need to complete this process again. 


## Side-note
If you want to add custom images to the Flux.1.dev model (i.e. fine-tune it) AND if you don't trust corporations with your data - there is a way to expand model locally, but you're gonna need at least **24 GB** of VRAM to do so. 

See: [ostris/ai-toolkit](https://github.com/ostris/ai-toolkit) & [Youtube Guide](https://www.youtube.com/watch?v=HzGW_Kyermg)

## Troubleshooting ('cuda' element is 'missing')
By default pip should download package 'torch==2.0.1+cu117', where 'cu117' - CUDA driver version supported by MY graphics card, '11.7'. 

I have no way to verify package / CUDA driver back-compatibility, so just in case, here's the instruction:

- To find CUDA driver version of your graphics card open Command line terminal (cmd.exe) and type: 'nvidia-smi' (NVIDIA graphics cards).

- Depending on that info you might want to downgrade or upgrade project packages to more suitable version. List of PyTorch ('torch') package versions can be found [here (latest)](https://pytorch.org/get-started/locally/) and [here (public archive)](https://pytorch.org/get-started/previous-versions/). 

- If you're using older PyTorch versions like me, you might experience some problems with 'cuda' element 'missing' on program launch - this means you've installed package that was compiled **without** CUDA driver support, so you'll need to uninstall it and look for a package with CUDA driver enabled. 

- In my case I had to 'build' my install script from scraps:

```ps
## taken from the public archive page - this is how we find latest package version for supported CUDA driver
# CUDA 11.7
pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1
## taken from the public archive page - this is how we find how to get package compiled with CUDA driver enabled
# CUDA 11.7
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
## Taken from the "get latest version" page - this is how we get correct command arguments syntax 
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

will result in:
```ps 
pip install torch==2.0.0+cu117 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu117
```

This might be difficult to understand at first, but this is how things are with public PyTorch archive, unfortunately.
