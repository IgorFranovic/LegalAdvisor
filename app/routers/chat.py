#app/routers/chat.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.gpt_service import generate_response
from app.database import SessionLocal
from app.models import Conversation
from typing import Optional

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = "default"

@router.post("/chat")
def chat_endpoint(request: PromptRequest):
    response_text = generate_response(request.prompt)
    
    db = SessionLocal()
    convo = Conversation(question=request.prompt, response=response_text)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    db.close()
    
    return {"response": response_text, "session_id": request.session_id}
