import requests
import streamlit as st


st.title("FastAPI TinyLlama ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Write your prompt in this input field"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = requests.get(f"http://localhost:8000/generate?prompt={prompt}").text
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
