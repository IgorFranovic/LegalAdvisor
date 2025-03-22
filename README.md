# LegalAdvisor
This is a simple legal advisor chatbot application that uses LLM integration


## Features

- LLM Integration: Uses OpenAI’s GPT-4o model (or your choice of model)
- Postgres Database: Stores conversations in the "conversations" table
- Docker-Compose: Spin up the entire stack (app + database) with one command
- Automatic Table Creation: Creates the table on startup if it doesn’t exist
- Provides a FastAPI implementation
- Provides a Streamlit-based UI that lets users send prompts and receive GPT-generated responses


## Project Structure

```
app/
├── main.py           # Initializes the database, sets up the FastAPI app, and includes the ‘chat’ router.
├── database.py       # Sets up SQLAlchemy engine & session
├── models.py         # Defines models used in the application
├── gpt_service.py    # Handles OpenAI API communication
├── streamlit_app.py  # Handles Streamlit logic
└── routers/
    └── chat.py       # Endpoints
.env                  # Environment variables (not committed to Git)
.env.example          # Example .env structure
docker-compose.yml    # Defines the postgress container and app service
Dockerfile.fastapi    # Builds a minimal Docker image for the FastAPI application
Dockerfile.streamlit  # Builds a Docker image for running the Streamlit UI
requirements.txt      # Python dependencies
```

## Docker Setup:

1. Clone the repository.
2. Create a `.env` file in the root with as shown in ```.env.example```   
3. Build and run using Docker Compose: ```docker-compose up --build``` \
   This starts a Postgres container, FastAPI (localhost:8000), Streamlit (localhost:8501)

Verifying Postgres Data:

The Postgres container data is stored in a named volume called pgdata, so your data persists even if the container restarts. You can connect to the database (for example, via psql or a GUI tool) using: Host: localhost Port: 5433

## Example Usage

Once you start the app with ```docker-compose up --build``` an instance of Streamlit will run on localhost:8501.
It communicates with the GPT service and the database through FastAPI calls.
You can send prompts and receive GPT generated responses.

```
Response to:
- What does it take to open up a law firm?
> Response: Starting a law firm involves several key steps and considerations:

Research and Planning:

Identify your practice area(s).
Research local market conditions and competition.
Develop a business plan detailing services, target clients, marketing strategy, financial projections, and growth plans.
...
```


A new row will appear in the "conversations" table.
