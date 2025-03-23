#app/routers/chat.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.gpt_service import generate_response, reset_conversation
from app.database import SessionLocal
from app.models import Conversation, ConversationSession
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = "default"

class SessionRequest(BaseModel):
    session_id: str

class SessionResponse(BaseModel):
    session_id: str
    created_at: str
    preview: str

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

@router.post("/reset")
def reset_endpoint(request: SessionRequest):
    # Reset the conversation memory for this session
    reset_conversation(request.session_id)
    
    return {"status": "success", "message": "Conversation reset successfully"}

@router.get("/chat-history/{session_id}")
def get_history(session_id: str):
    db = SessionLocal()
    
    # Get the session
    db_session = db.query(ConversationSession).filter(ConversationSession.session_id == session_id).first()
    
    if not db_session:
        db.close()
        return {"messages": []}
    
    # Get all messages for this session
    messages = db.query(Conversation).filter(Conversation.session_id == db_session.id).all()
    
    # Convert to a list of dictionaries
    message_list = [
        {"question": msg.question, "response": msg.response, "timestamp": msg.created_at}
        for msg in messages
    ]
    
    db.close()
    
    return {"messages": message_list}

@router.get("/sessions")
def get_sessions():
    db = SessionLocal()
    
    # Get all sessions ordered by last_updated (newest first)
    sessions = db.query(ConversationSession).order_by(ConversationSession.last_updated.desc()).all()
    
    result = []
    for session in sessions:
        # Get the first message for this session to use as preview
        first_message = db.query(Conversation).filter(
            Conversation.session_id == session.id
        ).order_by(Conversation.created_at.asc()).first()
        
        if first_message:
            # Create a preview from the first question (limited to 30 chars)
            preview = first_message.question[:30] + "..." if len(first_message.question) > 30 else first_message.question
            
            # Format created_at as a string
            created_at = session.created_at.strftime("%Y-%m-%d %H:%M")
            
            result.append({
                "session_id": session.session_id,
                "created_at": created_at,
                "preview": preview
            })
    
    db.close()
    
    return {"sessions": result}