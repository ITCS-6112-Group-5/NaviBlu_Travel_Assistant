# Hugging Face Space Entry Point for NaviBlu Travel Assistant

import streamlit as st
import os
from core import Chatbot
from dotenv import load_dotenv

load_dotenv()

# Avatar settings
USER_AVATAR = "👤"
ASSISTANT_AVATAR = "✈️"  # Travel-themed blue airplane

# Initialize chat history in streamlit session state
if "messages" not in st.session_state or st.session_state.messages is None:
    st.session_state.messages = []


# Initialize chatbot object in streamlit session state
if "chatbot" not in st.session_state or st.session_state.chatbot is None:
    st.session_state.chatbot = Chatbot()


# Streamlit App ----------------------------------------------------------------------

st.title("NaviBlu Travel Assistant")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type Here"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar=USER_AVATAR):
        # Display user query in UI
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):

        # Call shared chatbot logic
        response = st.session_state.chatbot.process_input(prompt) # type: ignore

        # Display response in UI
        st.markdown(response)

    # Add response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
