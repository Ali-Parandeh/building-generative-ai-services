import requests
import streamlit as st

st.title("FastAPI ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []


st.write("Upload a file to FastAPI")
file = st.file_uploader("Choose a file", type=["pdf"])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, bytes):
            st.audio(content)
        else:
            st.markdown(content)

if st.button("Submit"):
    if file is not None:
        files = {"file": (file.name, file, file.type)}
        response = requests.post("http://localhost:8000/upload", files=files)
        st.write(response.text)
    else:
        st.write("Please provide a file to upload")


if prompt := st.chat_input("Write your prompt in this input field"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        data = {"prompt": prompt, "model": "tinyllama", "temperature": 0.1}
        response = requests.post(
            f"http://localhost:8000/generate/text", json=data
        ).json()
        content = response["content"]
        st.markdown(content)

    st.session_state.messages.append({"role": "assistant", "content": content})
