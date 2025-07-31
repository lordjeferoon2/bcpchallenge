# app/prompts/customer_prompts.py

# Prompt para reconocer un saludo inicial
def get_greeting_response_prompt(user_message: str) -> str:
    return f"""
Eres un asistente financiero amable y servicial. El usuario acaba de escribir lo siguiente:

"{user_message}"

Responde de forma natural y cordial si parece un saludo. Si no parece un saludo, responde con un mensaje amable indicando que estás listo para ayudar.
"""

# Prompt para identificar el código de cliente en un mensaje libre
def extract_customer_id_prompt(user_message: str) -> str:
    return f"""
El siguiente mensaje fue enviado por el usuario: 
"{user_message}"

Tu tarea es detectar si incluye un código de cliente. 
Los códigos pueden tener letras y números (por ejemplo: CU-001, XZ55, cliente23). 
Devuelve solo el código exacto, sin explicación adicional. 
Si no hay ningún código, responde solo con la palabra: "NO_ENCONTRADO".
"""

def detect_intent_prompt(message: str) -> str:
    return f"""
Dado el siguiente mensaje de un usuario: "{message}"

Indica solo una palabra que representa su intención. Las opciones posibles son:
- saludo
- despedida
- reinicio
- pregunta
- sin_intencion

Responde con una sola palabra de las anteriores.
"""

# Prompt para generar el análisis financiero completo de un cliente
def generate_financial_analysis_prompt(customer: dict) -> str:
    loans = customer.get("loans", [])
    cards = customer.get("cards", [])
    scores = customer.get("credit_scores", [])
    cashflow = customer.get("cashflow", {})
    offers = customer.get("eligible_offers", [])

    last_score = scores[-1]["credit_score"] if scores else "Desconocido"

    loan_summary = "\n".join([
        f"- Préstamo {loan['loan_id']}: S/.{loan['principal']} a {loan['annual_rate_pct']}% anual, mora: {loan['days_past_due']} días"
        for loan in loans
    ]) or "No tiene préstamos activos."

    card_summary = "\n".join([
        f"- Tarjeta {card['card_id']}: saldo S/.{card['balance']} a {card['annual_rate_pct']}% anual, mora: {card['days_past_due']} días"
        for card in cards
    ]) or "No tiene tarjetas activas."

    income = cashflow.get("monthly_income_avg", "Desconocido")
    expenses = cashflow.get("essential_expenses_avg", "Desconocido")

    offer_summary = "\n".join([
        f"- Oferta {offer['offer_id']}: nueva tasa {offer['new_rate_pct']}% hasta {offer['max_term_months']} meses"
        for offer in offers
    ]) or "Actualmente no califica a ninguna oferta de consolidación."

    return f"""
Eres un asistente financiero bancario con acceso a inteligencia artificial generativa. A continuación, se presenta el perfil financiero de un cliente. Tu tarea es generar un **informe explicativo personalizado en lenguaje natural** que incluya los siguientes puntos:

### Datos del cliente:
- Score de crédito más reciente: {last_score}
- Ingresos mensuales promedio: S/.{income}
- Gastos esenciales promedio: S/.{expenses}

### Préstamos vigentes:
{loan_summary}

### Tarjetas de crédito vigentes:
{card_summary}

### Ofertas bancarias disponibles:
{offer_summary}

### Objetivo:
1. Generar **tres escenarios financieros** simulados para este cliente:
   - **Escenario 1 - Pago Mínimo**: Describe qué pasaría si el cliente solo realiza los pagos mínimos requeridos en sus productos financieros actuales.
   - **Escenario 2 - Plan Optimizado**: Diseña un plan de pagos priorizando productos con mayor tasa de interés y mora, utilizando el flujo de caja disponible del cliente.
   - **Escenario 3 - Consolidación**: Si el cliente califica, simula una consolidación de todas sus deudas usando las ofertas disponibles.

2. Para **cada escenario**, calcula o estima el **ahorro total comparado con el escenario de pago mínimo**.

3. Cierra el informe con una **recomendación clara y amigable**, escrita en un lenguaje fácil de entender para el cliente, resaltando cuál opción sería más beneficiosa y por qué.

Sé detallado, preciso y didáctico, como si le explicaras al cliente su situación y opciones de forma empática y profesional, no sobrepases de 500.
"""
