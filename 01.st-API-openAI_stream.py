# here using pure llama.cpp server with llama-server.exe -m .\model\tiny-vicuna-1b.q6_k.gguf -c 2048 --port 8001
import streamlit as st
# main: server is listening on http://127.0.0.1:8001 - starting the main loop
from openai import OpenAI
import datetime
import random
import string
import configparser
import tiktoken

def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read('tiny-vicuna-1b.ini',encoding='utf-8')
    # Access values from the configuration file
    NCTX = config.getint('Model', 'NCTX')
    modelname = config.get('Model', 'name')
    modelfile = config.get('Model', 'file')
    STOPS = config.get('Model', 'STOPS')
    myheader = config.get('UI', 'myheader')
    cursor = config.get('UI', 'cursor')
    av_us = config.get('UI', 'av_us')
    av_ass = config.get('UI', 'av_ass')
    # Return a dictionary with the retrieved value
    return NCTX,modelname,modelfile,STOPS,myheader,cursor,av_us,av_ass

NCTX,modelname,modelfile,STOPS,myheader,cursor,av_us,av_ass = read_config()

def writehistory(filename,text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

def countTokens(text):
    """
    Use tiktoken to count the number of tokens
    text -> str input
    Return -> int number of tokens counted
    """
    encoding = tiktoken.get_encoding("r50k_base") #context_count = len(encoding.encode(yourtext))
    numoftokens = len(encoding.encode(text))
    return numoftokens

#rewriting AVATARS  👷🐦  🥶🌀
av_us = 'user.png'  #or "🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass = 'assistant.png'

# Set the webpage title
st.set_page_config(
    page_title=f"Your LocalGPT with 🟠 {modelname}",
    page_icon="🟠",
    layout="wide")

# Create a header element
mytitle = f'<p style="color:Yellow; font-size: 32px;text-align:center;"><b>Your own LocalGPT</b></p>'
st.markdown(mytitle, unsafe_allow_html=True)
subtitle = f'<p style="color:DeepSkyBlue; font-size: 28px;text-align:center;"><b><i>{myheader}</i></b></p>'
st.markdown(subtitle, unsafe_allow_html=True)


def genRANstring(n):
    """
    n = int number of char to randomize
    """
    N = n
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=N))
    return res

# create THE SESSIoN STATES
if "logfilename" not in st.session_state:
## Logger file
    logfile = f'{genRANstring(5)}_log.txt'
    st.session_state.logfilename = logfile
    #Write in the history the first 2 sessions
    writehistory(st.session_state.logfilename,f'{str(datetime.datetime.now())}\n\nYour own LocalGPT with 🌀 {modelname}\n---\n🧠🫡: You are a helpful assistant.')    
    writehistory(st.session_state.logfilename,f'🌀: How may I help you today?')

if "len_context" not in st.session_state:
    st.session_state.len_context = 0

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.1

if "presence" not in st.session_state:
    st.session_state.presence = 1.2

if "maxlength" not in st.session_state:
    st.session_state.maxlength = 500

if "prompt" not in st.session_state:
    st.session_state.prompt =  ''

if "speed" not in st.session_state:
    st.session_state.speed =  0.0

# Point to the local server
# Change localhost with the IP ADDRESS of the computer acting as a server
# it may be something like "http://192.168.1.52:8001/v1"
# here using pure llama.cpp server with llama-server.exe -m models/OLMoE-1B-7B-0924-Instruct-Q4_K_L.gguf
client = OpenAI(base_url="http://localhost:8001/v1", api_key="not-needed", organization='SelectedModel')
 
# CREATE THE SIDEBAR
with st.sidebar:
    st.image('logo-small.png', use_container_width=True)
    st.session_state.temperature = st.slider('Temperature:', min_value=0.0, max_value=1.0, value=0.1, step=0.02)
    st.session_state.presence = st.slider('Penalty:', min_value=0.0, max_value=2.0, value=1.2, step=0.02)
    st.session_state.maxlength = st.slider('Length reply:', min_value=150, max_value=1000, 
                                           value=500, step=50)
    mytokens = st.markdown(f"""**Context turns** {st.session_state.len_context}""")
    st.markdown(f"**Logfile**: {st.session_state.logfilename}")
    st.markdown(f"`{modelfile}`")
    st.markdown(f"*Context tokens*: {NCTX}")
    speed = st.markdown(f"*generation speed*: {st.session_state.speed:.2f}  t/s")
    btnClear = st.button("Clear History",type="primary", use_container_width=True)

# We store the conversation in the session state.
# This will be used to render the chat conversation.
# We initialize it with the first message we want to be greeted with.

# CHANGE THE NAME OF THE AI IN THE SYSTEM PROMPT
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Tiny Vicuna 1B AI, a helpful assistant. You reply only to the user questions. You always reply in the language of the instructions.",}
    ]

# CHANGE THE NAME OF THE AI IN THE SYSTEM PROMPT
def clearHistory():
    st.session_state.messages = [
        {"role": "system", "content": "You are Tiny Vicuna 1B AI, a helpful assistant. You reply only to the user questions. You always reply in the language of the instructions.",}
    ]
    st.session_state.len_context = len(st.session_state.messages)
if btnClear:
      clearHistory()  
      st.session_state.len_context = len(st.session_state.messages)

# We loop through each message in the session state and render it as
# a chat message.
for message in st.session_state.messages[1:]:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar=av_ass):
            st.markdown(message["content"])

# We take questions/instructions from the chat input to pass to the LLM
if user_prompt := st.chat_input("Your message here. Shift+Enter to add a new line", key="user_input"):

    # Add our input to the session state
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )
    st.session_state.prompt = f"A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {user_prompt} ASSISTANT:"
    # Add our input to the chat window
    with st.chat_message("user", avatar=av_us):
        st.markdown(user_prompt)
        writehistory(st.session_state.logfilename,f'👷: {user_prompt}')
   
    with st.chat_message("assistant",avatar=av_ass):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            response = ''
            conv_messages = []
            full_response = ""
            start = datetime.datetime.now()
            # https://platform.openai.com/docs/api-reference/introduction
            # https://cookbook.openai.com/examples/how_to_stream_completions
            for items in client.completions.create(
                            prompt =st.session_state.prompt,
                            model=modelname,
                            temperature=st.session_state.temperature,
                            presence_penalty=st.session_state.presence,
                            stop=STOPS,
                            max_tokens=st.session_state.maxlength,              
                            stream=True):
                full_response += items.content
                message_placeholder.markdown(full_response + cursor)
            message_placeholder.markdown(full_response)
            delta = datetime.datetime.now() -start
            writehistory(st.session_state.logfilename,f'{cursor}: {full_response}\n\n---\n\n')         
            totalseconds = delta.total_seconds()
            prompttokens = countTokens(st.session_state.prompt)
            assistanttokens = countTokens(full_response)
            totaltokens = prompttokens + assistanttokens
            st.session_state.speed = totaltokens/totalseconds    
    # Add the response to the session state
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
    speed.markdown(f"*generation speed*: {st.session_state.speed:.2f}  t/s")
    st.session_state.len_context = len(st.session_state.messages)
