import streamlit as st
import requests
from typing import List
from streamlit_chat import message

st.set_page_config(page_title="ChatGPT", page_icon=":speech_balloon:", layout="wide")
st.title("ChatGPT")

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "我是一个疯狂的天才科学家，你有什么要问我的"}]

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
for message_obj in st.session_state.messages:
    message(message_obj["content"], is_user=(message_obj["role"] == "user"))

# Get user input
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
input_container = st.empty()
st.text_input("Ask something:", key="user_input", on_change=submit_message, value=st.session_state.user_input)
