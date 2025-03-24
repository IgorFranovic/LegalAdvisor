#app/routers/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ValidationError
from app.langchain.gpt_service import generate_response, reset_conversation
from app.data.database import SessionLocal
from app.data.models import Conversation, ConversationSession
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat")
def chat_endpoint(request: PromptRequest, db: Session = Depends(get_db)):
    try:
        if not request.prompt or request.prompt.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt cannot be empty"
            )
            
        # Generate the response
        try:
            response_text = generate_response(request.prompt, request.session_id)
        except Exception as e:
            logger.error(f"LLM service error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Error generating response from language model service"
            )
        
        # Get or create the conversation session
        try:
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
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred while saving conversation"
            )
        
        return {"response": response_text, "session_id": request.session_id}
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

def get_or_create_conversation_session(db: Session, session_id: str):
    """Get an existing session or create a new one"""
    try:
        db_session = db.query(ConversationSession).filter(ConversationSession.session_id == session_id).first()
        if not db_session:
            db_session = ConversationSession(session_id=session_id)
            db.add(db_session)
            db.commit()
            db.refresh(db_session)
        return db_session
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in get_or_create_conversation_session: {str(e)}")
        raise

@router.post("/reset")
def reset_endpoint(request: SessionRequest):
    try:
        # Validate session_id
        if not request.session_id or request.session_id.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID cannot be empty"
            )
            
        # Reset the conversation memory for this session
        try:
            reset_conversation(request.session_id)
        except Exception as e:
            logger.error(f"Error resetting conversation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error resetting conversation memory"
            )
        
        return {"status": "success", "message": "Conversation reset successfully"}
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in reset endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.get("/chat-history/{session_id}")
def get_history(session_id: str, db: Session = Depends(get_db)):
    try:
        if not session_id or session_id.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID cannot be empty"
            )
            
        try:
            # Get the session
            db_session = db.query(ConversationSession).filter(ConversationSession.session_id == session_id).first()
            
            if not db_session:
                return {"messages": []}
            
            # Get all messages for this session
            messages = db.query(Conversation).filter(Conversation.session_id == db_session.id).all()
            
            # Convert to a list of dictionaries
            message_list = [
                {"question": msg.question, "response": msg.response, "timestamp": msg.created_at}
                for msg in messages
            ]
            
            return {"messages": message_list}
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_history: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred while fetching chat history"
            )
    except Exception as e:
        logger.error(f"Unexpected error in get_history endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    try:
        try:
            # Get all sessions ordered by last_updated (newest first)
            sessions = db.query(ConversationSession).order_by(ConversationSession.last_updated.desc()).all()
            
            result = []
            for session in sessions:
                # Get the first message for this session to use as preview
                first_message = db.query(Conversation).filter(
                    Conversation.session_id == session.id
                ).order_by(Conversation.created_at.asc()).first()
                
                if first_message:
                    # Create a preview from the first question (limited to 150 chars)
                    preview = first_message.question[:150] + "..." if len(first_message.question) > 150 else first_message.question
                    
                    # Format created_at as a string
                    created_at = session.created_at.strftime("%Y-%m-%d %H:%M")
                    
                    result.append({
                        "session_id": session.session_id,
                        "created_at": created_at,
                        "preview": preview
                    })
            
            return {"sessions": result}
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_sessions: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred while fetching sessions"
            )
    except Exception as e:
        logger.error(f"Unexpected error in get_sessions endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )