# Ez_Flux1.dev
Super-lightweight and easy-to-use terminal shell for Flux.1 image generation model, created for people 
who like light-weight solutions with full control over everything happening in the code.

Current state of the project: everything is working as expected; tested on NVIDA RTX 3080 Ti mobile GPU 16 GB + 32GB RAM; additional features and better optimization logic is in progress.


## Features 
+ Image generation on demand (obviously)
+ Everythng is customizeable
+ Fully-automatic file name generation system & file saving
+ Fully-automatic call history logging (can be disabled during first launch or inside [settings](/program/config/appsettings.ini))
+ Can be used on machines with borked / outdated GPU driver and on machines with low VRAM (don't expect any miracles though)


## Features in development
+ ~~New pipeline configuration options~~
+ ~~Live image generator parameters change (without program restarts)~~


## Setup

### Python packages
Open powershell / bash terminal inside project folder, execute following command, it should install most packages automatically:
```ps
pip install -r requirement.txt
```
Note that I used Python 3.10.6 to run this project.

### Generative model
Before you get to play with image generator, the model needs to downloaded on your local hard drive. 
The download process is semi-automatic / guided. 

> Both 'schnell' and 'dev' models use **30~40 GB** of free disk space by default (each). 

#### !!! How to get & set huggingface access token (for 'Dev' model): 
+ Open [Flux1.dev webpage](https://huggingface.co/black-forest-labs/FLUX.1-dev) in your browser
+ Log in or Sign Up, agree to model access terms
+ Click on your avatar, open Settings page
+ Select Access Tokens and press "Create New Token"
+ In "token type" bar select "Read", add token name and click "Create token"
+ Keep page open for now, you'll need to copy access token later
+ Back in the project: open [config catalog](/program/config/)
+ Open file "user_secrets.md", copy everything inside
+ Create a new file "user_secrets.py" and paste text from a previous step
+ Copy your access token from huggingface webpage and replace value inside marked quotes '...', save and close the file


## How to use
+ Open project folder with VSCode or whichever code editor you're using
+ Run [main.py](main.py) script (I'm using **Python 3.10.6** for package compatibility)
+ Follow the instructions on screen (if any)
+ After successful load of the Flux.1 model you'll be asked to "enter your prompt" - type your desired request. Empty and whitespace-only requests will be automatically handled by the program as invalid. 
+ If you wish to exit the program type "exit" instead of your request - or simply kill the process, should free-up system memory either way.
+ If you wish to change flux call parameters (aspect ratio, image resolution, guidance scale, number of steps) - you can do this on startup, 
or in the main menu - type "menu" when the program asking for a prompt.


## Changing model call parameters
This option is available on program launch and in 'menu', right inside the terminal shell.

If you wish to change **DEFAULT** values (instead of session-only settings), 
here's one of the methods on how you can do so:
+ Open [FluxConfigurationProvider.py](/program/FluxConfigurationProvider.py)
+ Look for a line `def __init__ ....`, in brackets you'll find call parameters.
+ Change paraments to your liking, description for each parameter is provided above, in the same file


## Switching between models
Open [settings](/program/config/appsettings.ini) and set value of "initilized" variable to False, i.e. `initilized = False` and then launch / restart the program. 

Note that old model will not be deleted this way, in order to switch back you'll need to complete this process again. 


## Fine-tuning Flux.1
If you want to add custom images to the Flux.1.dev model (i.e. fine-tune it) AND if you don't trust corporations with your data - there is a way to expand model locally, but you're gonna need at least **24 GB** of VRAM to do so. 

See: [ostris/ai-toolkit](https://github.com/ostris/ai-toolkit) & [Youtube Guide](https://www.youtube.com/watch?v=HzGW_Kyermg)


## Troubleshooting 
Quick guide on how to solve known issues. 

If your issue is not listed in this section, please create "New Issue" on [official GitHub page](https://github.com/HardcoreMagazine/Ez_Flux.1/issues).

### Changing default model download (cache) path
By default huggingface library caches all models inside `C:\Users\%your_username%\.cache\huggingface\` catalog. 

If you're using separate hard drives for storing files and OS and / or you're low on free hard drive space - you can change the default cache location by creating 'HF_HOME' user / environment variable. 

Here's how to do this on Windows OS:
+ Open 'This Computer' or 'My Computer'
+ Right-click on empty space inside opened window, select 'Properties'
+ On your left click 'Advanced system settings'
+ In newly opened window look for 'User variables for %your_username%'
+ Click 'New...'
+ Inside 'Variable name' field input `HF_HOME`
+ Inside 'Variable value' field input path to desired cache location, for example: `D:\NeuralNetworks\huggingface` (note that 'huggingface' catalog has to be created manually)
+ Click 'OK', 'OK', 'OK', close the 'System' window
+ Restart your VSCode to apply changes (or whichever terminal or code editor you're using)

If you already have something downloaded inside the default cache location - simply move all contents of 'huggingface' catalog into inside newly created 'huggingface' folder at your desired cache location.

### 'Cuda' element is 'missing' - on program launch
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
