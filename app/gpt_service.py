#app/gpt_service.py

import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# for the direct openai api call
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

LEGAL_PROMPT = '''
You are a specialized legal assistant with expertise across various legal disciplines, 
tasked with offering general legal information and guidance. Please note:
1. You are not a licensed attorney and cannot provide personalized legal advice.
2. You should always advise consulting a qualified attorney for specific legal issues.
3. You may provide details on general legal concepts, processes, and regulations.
4. When addressing legal matters, include citations to relevant statutes, regulations, or case law as appropriate.
5. Ensure that your responses are clear, concise, and objective.
'''
# Create a dictionary to store message history objects by session_id
history_store = {}

def get_message_history(session_id):
    """Retrieve or create a message history object for a session"""
    if session_id not in history_store:
        history_store[session_id] = ChatMessageHistory()
    return history_store[session_id]

def generate_response(prompt: str, session_id: str = "default") -> str:
    """Generate a response using LangChain and message history"""
    
    llm = ChatOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-4o",  
        temperature=0.7
    )

    # Get message history for this session
    message_history = get_message_history(session_id)
    
    # Create message list, starting with system message
    messages = [SystemMessage(content=LEGAL_PROMPT)]
    
    # Add chat history
    messages.extend(message_history.messages)
    
    # Add the new user message
    messages.append(HumanMessage(content=prompt))
    
    # Generate response directly with the LLM
    response = llm.invoke(messages)
    
    # Update message history with the new exchange
    message_history.add_user_message(prompt)
    message_history.add_ai_message(response.content)
    
    return response.content.strip()

def reset_conversation(session_id: str):
    """Clear the conversation history for a given session"""
    if session_id in history_store:
        del history_store[session_id]

# Direct OpenAI API call
def generate_response_direct(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o", # Replace with desired model
        instructions="You are a helpful legal assistant.",
        input=prompt,
    )
    return response.output_text.strip()