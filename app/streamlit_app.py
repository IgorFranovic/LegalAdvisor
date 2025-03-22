#app/streamlit_app.py
import streamlit as st
import requests

st.title("Chat with a legal advisor")

# Input box for user prompt
prompt = st.text_area("Enter your prompt:")

if st.button("Submit"):
    if prompt.strip():
        response = requests.post(
            "http://fastapi:8000/chat",  # FastAPI container name
            json={"prompt": prompt}      # Send as JSON
        )

        if response.status_code == 200:
            st.write("Response:", response.json()["response"])
        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
