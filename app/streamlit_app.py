#app/streamlit_app.py
import streamlit as st
import requests
import uuid

# Initialize session state for conversation history if it doesn't exist
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Chat with a legal advisor")

# Display the conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Input box for user prompt
prompt = st.chat_input("Ask your legal question:")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    st.chat_message("user").write(prompt)
    
    # Prepare the loading message
    with st.chat_message("assistant"):
        response_container = st.empty()
        response_container.write("Thinking...")
        
        # Send request to API
        response = requests.post(
            "http://fastapi:8000/chat",  # FastAPI container name
            json={
                "prompt": prompt,
                "session_id": st.session_state.session_id
            }
        )
        
        if response.status_code == 200:
            response_text = response.json()["response"]
            # Update the assistant message
            response_container.write(response_text)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            response_container.write(f"Error from API: {response.status_code} - {response.text}")

# Function to start a new conversation
def start_new_conversation():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.rerun()

# Button to start a new conversation
if st.button("Start New Conversation"):
    start_new_conversation()