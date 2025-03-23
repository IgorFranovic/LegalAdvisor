#app/streamlit/streamlit_app.py
import streamlit as st
import requests
import uuid
import datetime
import os
# Initialize session state for conversation history if it doesn't exist
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
if "messages" not in st.session_state:
    st.session_state.messages = []

if "sessions_list" not in st.session_state:
    st.session_state.sessions_list = []

# Function to start a new conversation
def start_new_conversation():
    # Clear the messages and create a new session ID
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    # Force Streamlit to completely rerun the script
    st.rerun()

# Function to load a conversation by session_id
def load_conversation(session_id):
    # Set the session_id in the session state
    st.session_state.session_id = session_id
    
    # Fetch conversation history from API
    response = requests.get(f"http://fastapi:8000/chat-history/{session_id}")
    
    if response.status_code == 200:
        data = response.json()
        # Clear current messages
        st.session_state.messages = []
        
        # Add messages from history to session state
        for msg in data["messages"]:
            st.session_state.messages.append({"role": "user", "content": msg["question"]})
            st.session_state.messages.append({"role": "assistant", "content": msg["response"]})
        
        # Force Streamlit to rerun
        st.rerun()

# Fetch available sessions
def fetch_sessions():
    response = requests.get("http://fastapi:8000/sessions")
    if response.status_code == 200:
        # Return sessions already sorted by newest first
        return response.json()["sessions"]
    return []


import os

def load_css(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(script_dir, file_name)
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS
load_css('styles/style.css')

# Refresh sessions list
st.session_state.sessions_list = fetch_sessions()


# Sidebar for chat navigation
with st.sidebar:
    st.title("Conversations")
    
    
    # Handle the button click event
    if st.button("New Conversation", key="new_conv_button", use_container_width=True):
        start_new_conversation()
    
    st.divider()
    
    # Display previous conversations in sidebar
    if st.session_state.sessions_list:
        st.subheader("Recent Conversations")
        
        # For each session, create a column layout with buttons
        for session in st.session_state.sessions_list:
            # Extract preview (question) and date
            preview = session['preview']
            date_str = session['created_at']
            
            # Truncate preview if too long
            display_preview = preview[:25] + "..." if len(preview) > 25 else preview
            
            # Highlight current session
            button_type = "primary" if session['session_id'] == st.session_state.session_id else "secondary"
            
            # Create a container for this session
            session_container = st.container()
            with session_container:


                 # Add the date above the button
                st.markdown(f'<div class="small-date">{date_str}</div>', unsafe_allow_html=True)

                # Create a tooltip for the button
                tooltip = preview  # Full text as tooltip
                
                # Create a button with truncated question text
                if st.button(
                    f"**{display_preview}**", 
                    key=f"session_{session['session_id']}", 
                    use_container_width=True,
                    type=button_type,
                    help=tooltip
                ):
                    load_conversation(session['session_id'])
                
               
    else:
        st.info("No previous conversations")

# Main title
st.title("Chat with a legal advisor")

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
                
                # Refresh the sessions list immediately to include this session
                st.session_state.sessions_list = fetch_sessions()
            else:
                response_container.write(f"Error from API: {response.status_code} - {response.text}")