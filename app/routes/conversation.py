from fastapi import APIRouter, Request
from app.services.conversation_service import handle_user_message

router = APIRouter()

@router.post("/conversation")
async def conversation(request: Request):
    body = await request.json()
    message = body.get("message")
    session_id = body.get("session_id", "default")

    return handle_user_message(message, session_id)