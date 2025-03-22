# LegalAdvisor
This is a simple legal advisor chatbot application that uses LLM integration


## Features

- LLM Integration: Uses OpenAI’s GPT-4o model (or your choice of model)
- Postgres Database: Stores conversations in the "conversations" table
- Docker-Compose: Spin up the entire stack (app + database) with one command
- Automatic Table Creation: Creates the table on startup if it doesn’t exist
- Lays the foundation for a legal assistant chatbot

## Project Structure

```
app/
├── main.py           # Entry point – sends a sample prompt to GPT
├── database.py       # Sets up SQLAlchemy engine & session
├── models.py         # Defines models used in the application
└── gpt_service.py    # Handles OpenAI API communication
.env                  # Environment variables (not committed to Git)
.env.example          # Example .env structure
docker-compose.yml    # Defines the postgress container and app service
Dockerfile            # Builds a Python 3.9-slim image with dependencies
requirements.txt      # Python dependencies
```

## Docker Setup:

1. Clone the repository.
2. Create a `.env` file in the root with as shown in ```.env.example```   
3. Build and run using Docker Compose: ```docker-compose up --build``` \
   This starts a Postgres container and the app service

Verifying Postgres Data:

The Postgres container data is stored in a named volume called pgdata, so your data persists even if the container restarts. You can connect to the database (for example, via psql or a GUI tool) using: Host: localhost Port: 5433
---

## Example Output

```
Response to: Hello, how are you?
> I'm doing well, thank you! How can I assist you with your legal questions today?
```
A new row will appear in the "conversations" table.
