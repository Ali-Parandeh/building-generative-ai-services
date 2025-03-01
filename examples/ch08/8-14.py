# client.py

import requests
import streamlit as st

if st.button("Login with GitHub"):
    response = requests.get("http://localhost:8000/auth/oauth/github/login")
    if not response.ok:
        st.error("Failed to login with GitHub. Please try again later")
        response.raise_for_status()
