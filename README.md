# LegalAdvisor
This is a simple legal advisor chatbot application that uses LLM integration


## Features

- Integrates with OpenAI's GPT-4o model
- Sends a hardcoded prompt and prints the response to the terminal
- Lays the foundation for a legal assistant chatbot

## Project Structure

```
app/
├── main.py           # Entry point – sends a sample prompt to GPT
└── gpt_service.py    # Handles OpenAI API communication
.env                  # Stores the OPENAI_API_KEY (not committed to Git)
.env.example          # Example .env structure
```

## Setup

1. Clone the repository.
2. Create a `.env` file in the root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-key-here
   ```
3. Install dependencies:
   ```bash
   pip install openai python-dotenv
   ```
4. Run the app:
   ```bash
   python app/main.py
   ```

---

## Example Output

```
Response to: Hello, how are you?
> I'm doing well, thank you! How can I assist you with your legal questions today?
```
