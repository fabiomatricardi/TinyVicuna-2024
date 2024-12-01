

# TinyVicuna-2024
Run TinyVicuna-1B with streamlit and llama.cpp server


This small model is part of the TinyLlama project, that aims to pre-train a 1.1B Llama model on 3 trillion tokens with some proper optimization. But since Tiny Vicuna 1B is a TinyLLama 1.1B finetuned with WizardVicuna dataset it has been called Tiny-Vicuna!

This lightweight champion proves that size doesn't matter when it comes to brains. It sprints through NLP tasks with the grace of a cheetah, leaving bulkier models gasping in its dust. Think flawless summarization, precise question answering.

As a bonus… this model is under the Apache 2.0 license, and that means that 🥳
> The Apache software license gives users permission to reuse code for nearly any purpose, including using the code as part of proprietary software. As with other open source licenses, the Apache license governs how end-users can utilize the software in their own projects. This license is a widely-used open source license, and like other permissive licenses, it continues to grow in popularity because it encourages the use of open source software within proprietary projects.


### Requirements
After cloning the repo, create a virtual environment

I used Python 3.11
```
cd TinyVicuna-2024
python -m venv venv #I am using python 3.11
#to activate the Virtual Environment
source venv/bin/activate  #for mac
venv\Scripts\activate     #for windows users
```
Packages to be installed
```
pip install openai tiktoken streamlit==1.40.2
```

## Llama-server + openai API call
The main idea is that we will use the pre-compiled binaries of llama.cpp to run the fully compatible with the openAI API server

If you cloned the repo you already have the folder structure:
```
TinyVicuna-2024
├───llama.cpp
    └───model
```
- download and extract the llama.cpp binaries into the `llama.cpp` folder. I used llama-b4231-bin-win-vulkan-x64.zip
 from the official release [https://github.com/ggerganov/llama.cpp/releases/tag/b4231](https://github.com/ggerganov/llama.cpp/releases/tag/b4231)
- download the GGUF file 

### Code snipped

