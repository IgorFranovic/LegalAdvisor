# LegalAdvisor
This is a simple legal advisor chatbot application that uses LLM integration


## Features

- LLM Integration: Uses OpenAI’s GPT-4o model (or model of your choice)
- Stores conversations and sessions in a PostgreSQL database
- Docker integration: Spin up the entire stack (PostgreSQL Database, FastAPI API, Streamlit UI) with one command
- Provides a FastAPI implementation
- Provides a Streamlit-based UI that lets users send prompts and receive GPT-generated responses
- Uses LangChain's prompt templates for the legal advisor context
- Uses LangChain to maintain context between prompts
- Keeps track of conversation history (option to continue old conversations with context)

## Project Structure

```
app/
├── main.py                  # Initializes the database, sets up the FastAPI app, and includes the ‘chat’ router.
├── data/
|    ├── database.py         # Sets up SQLAlchemy engine & session  
|    └── models.py           # Defines models used in the application             
├── fastapi_routers/
|    └── chat.py             # FastAPI endpoints  
├── langchain/
|    └── gpt_service.py      # Handles OpenAI and Langchain logic 
└── streamlit/
     ├── streamlit_app.py    # Handles Streamlit logic  
     └── styles/              
          └── style.css      # CSS classes for Streamlit UI 

.env                         # Environment variables (not committed to Git)
.env.example                 # Example .env structure
docker-compose.yml           # Defines the postgress container and app service
Dockerfile.fastapi           # Builds a minimal Docker image for the FastAPI application
Dockerfile.streamlit         # Builds a Docker image for running the Streamlit UI
requirements.txt             # Python dependencies
```

## Docker Setup:

1. Clone the repository.
2. Create a `.env` file in the root with as shown in ```.env.example```   
3. Replace `OPENAI_API_KEY` value with a valid one.
4. You can leave the Postgre user, password and database name as is.
5. Build and run using Docker Compose: ```docker-compose up --build``` \
   This starts a Postgres container, launches FastAPI on `localhost:8000` and launches Streamlit on `localhost:8501`

Verifying Postgres Data:

The Postgres container data is stored in a named volume called pgdata, so the data persists even if the container restarts. You can connect to the database (for example, via psql or a GUI tool) using: 
Host: `localhost` 
Port: `5433` 
Copy the database name, user, password from your `.env` file.

If you want to remove the data, use: `docker-compose down -v`

## Example Usage

Once you start the app with ```docker-compose up --build```, an instance of Streamlit will run on ```localhost:8501```.
Navigate to the URL to interact with the app.

Ask questions using the prompt field on the bottom.
Navigate through previous conversations using the sidemenu on the left.

The `'New Conversation'` button creates a fresh session, not keeping any context from the previous one.


```
Example question to demonstrate system prompts:
- How do I file for bankruptcy?
> Response: Filing for bankruptcy is a complex legal process that involves several steps. Below is a general overview of the process in the United States, but it is crucial to consult with a qualified attorney to understand how the laws apply to your specific situation:
...
```


A new row will appear in the `conversations` table for each prompt. 
If a new session is started, a new row will appear in the `conversation_sessions` table.
