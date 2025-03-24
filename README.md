# LegalAdvisor

A legal advisor chatbot application that leverages OpenAI's GPT-4o model to provide general legal information and guidance through a user-friendly interface.

## Features

- **LLM Integration**: Uses OpenAI's GPT-4o model through LangChain
- **Persistent Storage**: Stores conversations and sessions in a PostgreSQL database
- **Docker Integration**: Easily deploy the entire stack (PostgreSQL, FastAPI, Streamlit) with one command
- **RESTful API**: FastAPI implementation for all backend operations
- **User-Friendly UI**: Streamlit-based interface for interacting with the chatbot
- **Context-Aware**: Maintains conversation history between prompts using LangChain
- **Session Management**: Ability to continue old conversations with full context

## Project Architecture

The application follows a three-tier architecture:

```
LegalAdvisor
├── Database Layer (PostgreSQL)
├── Backend Layer (FastAPI + LangChain)
└── Frontend Layer (Streamlit)
```

### Directory Structure

```
app/
├── main.py                  # FastAPI app initialization and database setup
├── data/
|    ├── database.py         # SQLAlchemy engine & session configuration  
|    └── models.py           # Database models for conversations and sessions             
├── fastapi_routers/
|    └── chat.py             # API endpoints for chat functionality 
├── langchain/
|    └── gpt_service.py      # LLM integration with OpenAI and conversation management 
└── streamlit/
     ├── streamlit_app.py    # Streamlit UI application 
     └── styles/              
          └── style.css      # CSS styling for Streamlit UI 

.env                         # Environment variables (not committed to Git)
.env.example                 # Example environment variable template
docker-compose.yml           # Docker services configuration
Dockerfile.fastapi           # Docker image for FastAPI service
Dockerfile.streamlit         # Docker image for Streamlit service
requirements.txt             # Python dependencies
```

## Legal Advisor Context Approach

The application uses a specialized system prompt (defined in `gpt_service.py`) that:

1. Establishes the assistant as a legal information provider, not a licensed attorney
2. Sets clear boundaries on what types of legal information can be provided
3. Requires disclaimers and attorney consultation recommendations
4. Enforces ethical guidelines to prevent misuse
5. Includes safeguards against prompt injection attempts

The system ensures that responses:
- Include citations to relevant laws where appropriate
- Remain objective and informational
- Advise users to consult qualified attorneys for specific cases
- Refuse requests for drafting legal documents or circumventing regulations

## Setup and Running Instructions

### Prerequisites

- Docker and Docker Compose installed on your system
- An OpenAI API key with access to the GPT-4o model

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/IgorFranovic/LegalAdvisor.git
   cd LegalAdvisor
   ```

2. **Create environment variables file**
   
   Copy the example environment file and edit it:
   ```bash
   cp .env.example .env
   ```

3. **Add your OpenAI API key**
   
   Edit the `.env` file and replace `your-key-here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key
   ```
   
   Note: You can keep the PostgreSQL credentials as they are for local development.

4. **Build and start the application**
   
   ```bash
   docker-compose up --build
   ```
   
   This command:
   - Builds Docker images for FastAPI and Streamlit
   - Creates and configures a PostgreSQL database
   - Starts all three services with proper networking

5. **Access the application**
   
   - Streamlit frontend: http://localhost:8501
   - FastAPI backend: http://localhost:8000
   - API documentation: http://localhost:8000/docs

### Running Services Individually

If you need to run services separately for development or troubleshooting:

#### Database Only

```bash
docker-compose up db
```

#### FastAPI Backend Only

Ensure the database is running first, then:

```bash
docker-compose up fastapi
```

#### Streamlit Frontend Only

Ensure the FastAPI service is running first, then:

```bash
docker-compose up streamlit
```

## Database Management

### Connecting to PostgreSQL

You can connect to the PostgreSQL database using a client tool (e.g., pgAdmin, DBeaver) with:

- Host: `localhost`
- Port: `5433` (Note: mapped from standard 5432 to avoid conflicts)
- Database: Value of `POSTGRES_DB` in your `.env` file
- Username: Value of `POSTGRES_USER` in your `.env` file
- Password: Value of `POSTGRES_PASSWORD` in your `.env` file

### Persistent Data

- Database data is stored in a named Docker volume `pgdata` for persistence
- To completely reset the database: `docker-compose down -v`

## Usage Guide

1. Navigate to http://localhost:8501 in your web browser
2. Type your legal question in the input field at the bottom
3. Receive AI-generated legal information based on your query
4. View previous conversations in the sidebar
5. Create a new conversation by clicking "New Conversation"

Example questions to try:
- "How do I file for bankruptcy?"
- "What are the steps to register a trademark?"
- "What is the difference between a will and a trust?"


## API Documentation

The FastAPI backend exposes the following endpoints:

- `POST /chat`: Send a message and receive a response
- `GET /chat-history/{session_id}`: Retrieve conversation history for a session
- `GET /sessions`: List all conversation sessions
- `POST /reset`: Reset a conversation session

Detailed API documentation is available at http://localhost:8000/docs when the application is running.

## Future Improvements

- Add user authentication
- Implement rate limiting
- Add support for document upload and analysis
- Expand the system prompt with more specialized legal domains
- Add unit and integration tests
