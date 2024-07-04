# img_to_libsync_cpr

Programms to install:

python
git
ffmpeg

img_to_libsync_cpr: https://github.com/CedrikRose/img_to_libsync_cpr.git
SadTalker: https://github.com/OpenTalker/SadTalker

if Cartoon filter is wanted:
Stable Diffusion: https://github.com/CompVis/stable-diffusion.git
lora model Cartoon portrait: https://civitai.com/api/download/models/120882


Installation:

install img_to_libsync_cpr
git clone https://github.com/CedrikRose/img_to_libsync_cpr.git

cd img_to_libsync_cpr

put the original CPR Video in the Folder
FY24 YM NOL NFL HOCPR ENG ESP CC.mp4

install requirements
pip install -r requirements.txt


SadTalker:

git clone https://github.com/OpenTalker/SadTalker.git

cd SadTalker 

conda create -n sadtalker python=3.8

conda activate sadtalker

pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113

conda install ffmpeg

pip install -r requirements.txt
important: in requirements.txt gradio==3.41.2


Stable Diffusion:

cd img_to_libsync_cpr

git clone https://github.com/CompVis/stable-diffusion.git

important: in img_to_libsync_cpr/stable diffusion/webui/webui-user.sh: line 13: #export COMMANDLINE_ARGS="--api --xformers --no-half"

the venv should install automaticly by running
img_to_libsync_cpr/stable diffusion/webui/webui-user.sh

download the lora in stable diffusion/webui/models/Lora/cartoonish_v1.safetensors
lora model Cartoon portrait: https://civitai.com/api/download/models/120882

if stable diffusion/webui/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors dose no already exist download it from:
https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors?download=true

