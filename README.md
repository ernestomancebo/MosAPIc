## Environment Setup
This is following over the internet. Also this requires conda.

1. Install miniconda.
1. Install conda dependencies
```bash 
conda create -n gpt4all python=3.10
conda activate gpt4all 
conda install -c conda-forge cmake
```
1. Install pip dependencies
```bash
pip install nomic gpt4all pygpt4all
```