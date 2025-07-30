# app/services/conversation_service.py

from app.prompts.customer_prompt import (
    extract_customer_id_prompt,
    generate_financial_analysis_prompt,
    get_greeting_response_prompt
)
from app.services.azure_openai_service import get_response_from_model
from app.services.customer_service import get_consolidated_customers
from typing import Dict

# Simulación de almacenamiento en memoria por sesión
session_states: Dict[str, Dict] = {}


def handle_user_message(message: str, session_id: str) -> str:
    if not message:
        return "Por favor envía un mensaje para que pueda ayudarte."

    # Obtener o inicializar estado de la sesión
    session = session_states.setdefault(session_id, {
        "stage": "greeting",
        "customer_id": None
    })

    stage = session["stage"]

    # STAGE 1: Saludo inicial
    if stage == "greeting":
        prompt = get_greeting_response_prompt(message)
        greeting = get_response_from_model(prompt)
        session["stage"] = "waiting_for_id"
        return f"{greeting} ¿Podrías indicarme tu código de cliente?"

    # STAGE 2: Esperando código de cliente
    elif stage == "waiting_for_id":
        prompt = extract_customer_id_prompt(message)
        client_id = get_response_from_model(prompt).strip()

        if client_id == "NO_ENCONTRADO":
            return "No pude identificar tu código de cliente. Por favor revísalo e intenta nuevamente."

        customers = get_consolidated_customers()
        matched = next((c for c in customers if c["customer_id"].upper() == client_id.upper()), None)

        if matched:
            session["stage"] = "evaluation_ready"
            session["customer_id"] = client_id.upper()
            prompt = generate_financial_analysis_prompt(matched)
            analysis = get_response_from_model(prompt)
            return analysis
        else:
            return f"No encontré un cliente con el código '{client_id}'. ¿Podrías verificarlo e intentarlo de nuevo?"

    # STAGE 3: Evaluación ya realizada, conversación continua
    elif stage == "evaluation_ready":
        if any(p in message.lower() for p in ["gracias", "ok", "listo", "perfecto"]):
            return "¡Con gusto! Si deseas volver a revisar tu información financiera o tienes alguna otra consulta, solo dime."

        return "Ya tengo tu información financiera registrada. ¿Deseas que revisemos algo más o necesitas ayuda adicional?"

    # Fallback
    return "Algo salió mal con la conversación. ¿Podrías repetir lo que necesitas?"
