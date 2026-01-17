# Hugging Face Space Entry Point for NaviBlu Travel Assistant

import streamlit as st
import os
from core import Chatbot
from dotenv import load_dotenv

load_dotenv()

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="NaviBlu Travel Assistant",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to reduce top padding
st.markdown("""
    <style>
    /* Reduce top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Reduce header spacing */
    header {
        padding-top: 0rem;
    }
    
    /* Adjust title spacing */
    h1 {
        padding-top: 0rem;
        margin-top: 0rem;
    }
    </style>
""", unsafe_allow_html=True)

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
st.write("Ask questions about flights, hotels, and travel destinations!")

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
