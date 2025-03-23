#app/gpt_service.py

import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

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

def generate_response(prompt: str) -> str:
    
    llm = ChatOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-4o",  
        temperature=0.7
    )

    # Define a simple prompt template
    prompt_template = ChatPromptTemplate.from_template(
        LEGAL_PROMPT + " The user says: {user_input}"
    )

    # Create a chain using the pipe operator
    chain = prompt_template | llm
    
    # Run the chain with the user's prompt using invoke
    response = chain.invoke({"user_input": prompt})
    
    # Extract the content from the response
    return response.content.strip()

# Direct OpenAI API call
def generate_response_direct(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o", # Replace with desired model
        instructions="You are a helpful legal assistant.",
        input=prompt,
    )
    return response.output_text.strip()


