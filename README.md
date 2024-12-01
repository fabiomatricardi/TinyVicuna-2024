<img src='https://github.com/fabiomatricardi/TinyVicuna-2024/raw/main/logo-small.png' width=800>

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
- download the GGUF file from the official afrideva repo: [tiny-vicuna-1b.q6_k.gguf](https://huggingface.co/afrideva/Tiny-Vicuna-1B-GGUF/resolve/main/tiny-vicuna-1b.q6_k.gguf)

### Code snipped
This is the basic code you need to talk to your API endpoint, powered by llama.server:

In one terminal, form the llama.cpp directory run
```
llama-server.exe -m .\model\tiny-vicuna-1b.q6_k.gguf -c 2048 --port 8001
```


In another terminal, the with venv activated, run python, and then copy paste the following:
```
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8001/v1", 
                api_key="not-needed", organization='SelectedModel')
user_prompt = 'what is Science?'
prompt = f"A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {user_prompt} ASSISTANT:"
stoptoken = '<s>'
for items in client.completions.create(
                prompt = prompt,
                model='tinyvicuna',
                temperature=0.15,
                presence_penalty=1.21,
                stop=stoptoken,
                max_tokens=500,              
                stream=True):
     print(items.content,end='',flush=True)
```

## Streamlit interface
Without closing the llama-server, in the second window run:
```
streamlit run .\01.st-API-openAI_stream.py
```
Remember to have cloned the repo, there are few images and an INI file required for the Streamlit app





