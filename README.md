# CreampuffBOT
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) ![python: 3.0+](https://img.shields.io/badge/python-3.0+-yellow.svg) ![poetry: 1.5+](https://img.shields.io/badge/poetry-1.5+-blue.svg) ![Git](https://img.shields.io/badge/Git-orange.svg)  
**CRK Guild Battle OCR Data Logger**    

This bot/program's purpose is to take a folder of screenshots containing guild battle hits from **Cookie Run: Kingdom** and serialize them into a `.csv` file to perform further data analysis on.

[Example output](https://pastebin.com/JWKAuT4M) for an average week's worth of hits.

## Install/Build Instructions
### Prerequisites
> [Git](https://git-scm.com/downloads) *Preinstalled on Macs and most Linux/Unix distros*  
> [Python (>3.0)](https://www.python.org/downloads/) *Note: make sure to add it to PATH (Windows)*  
> [Poetry](https://python-poetry.org/docs/#installation)  

<sub><sup>*if Python is installed, you can do `pip install poetry` and check your installation with `poetry --version`*</sup></sub>

### Dependencies
- To install the Python dependencies using Poetry, navigate to the project root directory `./CreampuffBOT` and run:
> `poetry install`

### Building
If you wish to examine the source code yourself and build it into an untested executable you can perform the following:
- From the `src` folder: `pyinstaller --onefile --windowed --additional-hooks-dir=. gui.py`

## GPU / CUDA Info
- This program is intended to be run on CUDA compatible GPUs. Because this program does a lot with image processing: having a GPU that can be properly taken
advantage of by the program will dramatically improve runtime.  
- *Is my GPU CUDA compatible?* -- Most NVIDIA graphics cards *are* CUDA compatible. AMD cards are *not* compatible. Intel cards also do not currently support CUDA.
For more information and to check if your card is compatible, check here: https://developer.nvidia.com/cuda-gpus


### CUDA Installations
To take advantage of your GPU, you will need to have a few things downloaded:
1. Your drivers should be up to date. https://www.nvidia.com/download/index.aspx
2. The CUDA toolkit needs to be installed. https://developer.nvidia.com/cuda-toolkit
3. PyTorch (CUDA) must be installed. https://pytorch.org/get-started/locally/  
The command for Windows + CUDA 11.7 was `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117` -- this may vary.
- To check your installation, you can run these two commands in a python shell to test if you can successfully utilize your GPU with this program.
```
import torch
torch.cuda.is_available()
```
