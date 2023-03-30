import streamlit as st
import requests
from typing import List

st.set_page_config(page_title="ChatGPT", page_icon=":speech_balloon:", layout="wide")
st.title("ChatGPT")

def display_messages(messages: List[dict]):
    for message in messages:
        if message["role"] == "user":
            st.write(f"<div style='text-align: right; color: blue;'>{message['content']}</div>", unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.write(f"<div style='text-align: left; color: green;'>{message['content']}</div>", unsafe_allow_html=True)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "你是一个有用的助手"}]

# Define submit_message function
def submit_message():
    initialize_session_state()
    if st.session_state.user_input:
        # Update chat history
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
        
        # Send request and receive response
        response = requests.post("http://localhost:8000/chat", json={"messages": st.session_state.messages})
        chat_response = response.json()["response"]
        st.session_state.messages.append({"role": "assistant", "content": chat_response})

        # Clear user input
        st.session_state.user_input = ""

        # Refresh the input widget
        refresh_key = int(st.experimental_get_query_params().get("refresh_key", [0])[0]) + 1
        st.experimental_set_query_params(refresh_key=refresh_key)

initialize_session_state()

# Display chat history
display_messages(st.session_state.messages)

# Get user input
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
input_container = st.empty()
input_container.text_input("Ask something:", key="user_input", on_change=submit_message, value=st.session_state.user_input)
