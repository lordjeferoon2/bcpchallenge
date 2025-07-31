from fastapi import APIRouter, Body
from typing import Dict
from app.services.conversation_service import handle_user_message

router = APIRouter(prefix="/chat", tags=["Conversación"])

@router.post(
    "/conversation",
    summary="Iniciar conversación con el LLM",
    description="""
Este endpoint inicia o continúa una conversación con el modelo de lenguaje (LLM).

Debes enviar un mensaje y un `session_id`. El flujo de la conversación se adapta dependiendo del estado del usuario (saludo, identificación, evaluación, etc.).
""",
    response_description="Respuesta generada por el modelo LLM"
)
async def conversation(
    body: Dict = Body(
        ...,
        example={
            "message": "Hola, quiero revisar mis finanzas",
            "session_id": "abc123"
        }
    )
):
    message = body.get("message")
    session_id = body.get("session_id", "default")
    return handle_user_message(message, session_id)