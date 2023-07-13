

import openai
import streamlit as st
from streamlit_chat import message
import re
import os
import json

count = 0
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(prompt):

   messages = [{"role": "user", "content": prompt}]
   functions = [
    {
        "name": "empathise",
        "description": "Generate text which empathises with the user",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description" : "The generated text to empathize with the user",
                }
            },
            "required": ["text"]
        },
    },
    {
        "name": "backup_assistant",
        "description": "Generate text which will act as an all-time assistant",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description" : "The generated counter question to the user's input",
                }
            },
            "required": ["text"]
        },
    },
    {
        "name": "recommend_content",
        "description": "Generate text which recommends self-help books and podcasts",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description" : "The generated text for the recommendation",
                }
            },
            "required": ["text"]
        },
    }
              ]

   response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )

   try:
       # Extract the function call arguments, which is a stringified JSON
       function_args_json = response['choices'][0]['message']['function_call']['arguments']

       # Parse the stringified JSON to get a Python dict
       function_args = json.loads(function_args_json)

       # Extract the text from the parsed JSON
       text = function_args['text']
       print("THE FUNCTION WAS CALLED")
   except KeyError:
       # Handle the case when 'function_call' does not exist in the message
       text = response['choices'][0]['message']['content']

   print(text)
   print("THE OPENAI API WAS CALLED")

   return text
   


# EXECUTION OF THE PROGRAM STARTS HERE

st.title("Mental Health Bot")
st.info("Yo I'm here for you always you know this")


# Storing the chat

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

prompt = get_text()
print("The prompt is :", prompt)

if prompt:
    output = generate_response(prompt)
    # Save the output
    st.session_state.past.append(prompt)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        message(st.session_state['generated'][i], key = str(i))
        message(st.session_state['past'][i], is_user =True, key=str(i)+ '_user')
