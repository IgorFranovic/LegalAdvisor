#app/streamlit_app.py
import streamlit as st
import requests
import uuid

# Initialize session state for conversation history if it doesn't exist
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to start a new conversation
def start_new_conversation():
    # Clear the messages and create a new session ID
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    # Force Streamlit to completely rerun the script
    st.rerun()

# Create a layout with title and button side by side
col1, col2 = st.columns([3, 1])

with col1:
    st.title("Chat with a legal advisor")

with col2:
    # Add more vertical space to align better with the title
    st.write("")
    st.write("")
    if st.button("New Chat"):
        start_new_conversation()

# Create a scrollable container for the chat messages
chat_container = st.container(height=400)

# Clear the container before adding new content
with chat_container:
    st.empty()
    
    # Display the conversation history inside the scrollable container
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
    
    # Display user message in the scrollable container
    with chat_container:
        st.chat_message("user").write(prompt)
    
    # Prepare the loading message
    with chat_container:
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