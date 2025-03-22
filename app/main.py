#app/main.py

from gpt_service import generate_response

if __name__ == "__main__":
    user_input = "Hello, how are you?"
    response = generate_response(user_input)
    print(response)