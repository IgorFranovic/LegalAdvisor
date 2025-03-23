#app/routers/chat.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.gpt_service import generate_response
from app.database import SessionLocal
from app.models import Conversation, ConversationSession
from typing import Optional
from sqlalchemy.orm import Session

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = "default"



@router.post("/chat")
def chat_endpoint(request: PromptRequest):
    response_text = generate_response(request.prompt, request.session_id)
    
    db = SessionLocal()
    
    # Get or create the conversation session
    db_session = get_or_create_conversation_session(db, request.session_id)
    
    # Add the new message
    convo = Conversation(
        session_id=db_session.id,
        question=request.prompt, 
        response=response_text
    )
    
    db.add(convo)
    db.commit()
    db.refresh(convo)
    db.close()
    
    return {"response": response_text, "session_id": request.session_id}


def get_or_create_conversation_session(db: Session, session_id: str):
    """Get an existing session or create a new one"""
    db_session = db.query(ConversationSession).filter(ConversationSession.session_id == session_id).first()
    if not db_session:
        db_session = ConversationSession(session_id=session_id)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
    return db_session