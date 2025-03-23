#app/gpt_service.py

import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

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
# Create a dictionary to store memory objects by session_id
memory_store = {}

def get_memory(session_id):
    """Retrieve or create a memory object for a session"""
    if session_id not in memory_store:
        memory_store[session_id] = ConversationBufferMemory()
    return memory_store[session_id]

def generate_response(prompt: str, session_id: str = "default") -> str:
    """Generate a response using LangChain's conversation memory"""
    
    llm = ChatOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-4o",  
        temperature=0.7
    )

    # Get or create memory for this session
    memory = get_memory(session_id)
    
    # Create a conversation chain with memory
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    # Add the legal prompt context to the user input
    full_prompt = f"{LEGAL_PROMPT}\n\nUser: {prompt}"
    
    # Generate response
    response = conversation.predict(input=full_prompt)
    
    return response.strip()

# Direct OpenAI API call
def generate_response_direct(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o", # Replace with desired model
        instructions="You are a helpful legal assistant.",
        input=prompt,
    )
    return response.output_text.strip()


