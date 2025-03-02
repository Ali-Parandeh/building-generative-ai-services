# client.py

import requests
import streamlit as st

...

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.image(message["content"])
...

if prompt := st.chat_input("Write your prompt in this input field"):
    ...
    response = requests.get(
        f"http://localhost:8000/generate/image", params={"prompt": prompt}
    )
    response.raise_for_status()
    with st.chat_message("assistant"):
        st.text("Here is your generated image")
        st.image(response.content)

    ...
