#app/gpt_service.py

import os
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def generate_response(prompt: str) -> str:
    
    llm = ChatOpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-4o",  
        temperature=0.7
    )

    # Define a simple prompt template
    prompt_template = ChatPromptTemplate.from_template(
        "You are a helpful legal assistant. The user says: {user_input}"
    )

    # Create a chain that ties the prompt to the LLM
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Run the chain with the user's prompt
    output = chain.run({"user_input": prompt})
    return output.strip()

# Direct OpenAI API call
def generate_response_direct(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o", # Replace with desired model
        instructions="You are a helpful legal assistant.",
        input=prompt,
    )
    return response.output_text.strip()


