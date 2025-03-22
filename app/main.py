#app/main.py

from gpt_service import generate_response
from database import SessionLocal, engine
from models import Base, Conversation


def init_db():
    Base.metadata.create_all(bind=engine)  # Create all tables


if __name__ == "__main__":

    # Create tables on startup
    init_db()

    user_input = "Hello, how are you?"
    response_text = generate_response(user_input)
    print(response_text)

    
    db = SessionLocal()
    convo = Conversation(question=user_input, response=response_text)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    db.close()
