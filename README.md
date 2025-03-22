# LegalAdvisor
This is a simple legal advisor chatbot application that uses LLM integration


## Features

- LLM Integration: Uses OpenAI’s GPT-4o model (or your choice of model)
- Postgres Database: Stores conversations in the "conversations" table
- Docker-Compose: Spin up the entire stack (app + database) with one command
- Automatic Table Creation: Creates the table on startup if it doesn’t exist
- Provides a FastAPI implementation


## Project Structure

```
app/
├── main.py           # Initializes the database, sets up the FastAPI app, and includes the ‘chat’ router.
├── database.py       # Sets up SQLAlchemy engine & session
├── models.py         # Defines models used in the application
├── gpt_service.py    # Handles OpenAI API communication
└── routers/
    └── chat.py       # Endpoints
.env                  # Environment variables (not committed to Git)
.env.example          # Example .env structure
docker-compose.yml    # Defines the postgress container and app service
Dockerfile.fastapi    # Builds a minimal Docker image for the FastAPI application
requirements.txt      # Python dependencies
```

## Docker Setup:

1. Clone the repository.
2. Create a `.env` file in the root with as shown in ```.env.example```   
3. Build and run using Docker Compose: ```docker-compose up --build``` \
   This starts a Postgres container and the app service

Verifying Postgres Data:

The Postgres container data is stored in a named volume called pgdata, so your data persists even if the container restarts. You can connect to the database (for example, via psql or a GUI tool) using: Host: localhost Port: 5433

## Example Output

Once you start the app with ```docker-compose up --build``` an instance of FastAPI will run on localhost:8000.
You can target the ```/chat``` endpoint with Postman (or similar tools). Pass a json in a post request body containing a string "prompt".

```
Response to:
{
    "prompt": "Hello from Postman, how are you?"
}
> "Hello! I'm here to help. How can I assist you today?"
```
A new row will appear in the "conversations" table.
