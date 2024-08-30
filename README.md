# Ez_Flux1.dev
Super light-weight and easy-to-use terminal shell for Flux.1 image generation model created for people 
who like light-weight solutions with full control over everything happenig in the code.

## Features 
+ Image generation on demand (obviously)
+ Can be customized (requires coding skills)
+ Fully-automatic file name generation system & file saving
+ Fully-automatic call history logging (can be disabled inside [settings](/program/config/appsettings.ini))
+ Can be used on machines with borked / outdated GPU driver and on low VRAM machines (don't expect any miracles though)

## First setup (important)
Before you get to play with Flux.1 image generator, the model needs to downloaded on your local hard drive. 
The download process is semi-automatic / guided. 

> Note that the 'Dev' model uses **~32 GB** of free disk space. 

### How to get huggingface access token (for 'Dev' model): 
+ Open [Flux1.dev webpage](https://huggingface.co/black-forest-labs/FLUX.1-dev) in your browser
+ Log in or Sign Up, agree to model access terms
+ Click on your avatar, open Settings page
+ Select Access Tokens and press "Create New Token"
+ In "token type" bar select "Read", add token name and click "Create token"
+ Keep page open for now, you'll need to copy access token later
+ Back in the project: open [config](/program/config/) catalog
+ Open file "user_secrets.md", copy everything inside
+ Create a new file with name: "user_secrets.py" and paste contents of "md" file
+ Copy your access token from huggingface webpage and paste it inside empty quotes <''>, save and close the file

## How to use
+ Open project folder with VSCode or whichever editor you're using
+ Run [main.py](main.py) script (I'm using **Python 3.10.6**)
+ After successful load of the Flux1.dev model you'll be asked to "enter your prompt" - type your desired request. Empty and whitespace-only requests will be automatically handled by the program. 
+ If you wish to exit the program type "exit" instead of your request - or simply kill the process, should free-up memory either way.

## Side-note
If you want to add custom images to the Flux1.dev model (i.e. fine-tune it) AND if you don't trust corporations with your data - there is a way to expand model locally, but you're gonna need at least **24 GB** of VRAM to do so. 

See: [ostris/ai-toolkit](https://github.com/ostris/ai-toolkit) & [Youtube Guide](https://www.youtube.com/watch?v=HzGW_Kyermg)