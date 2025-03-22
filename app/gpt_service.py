#app/gpt_service.py

import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv() # Load environment variables from the .env file

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def generate_response(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o", # Replace with desired model
        instructions="You are a helpful legal assistant.",
        input=prompt,
    )
    return response.output_text.strip()
