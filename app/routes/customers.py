from fastapi import APIRouter
from typing import List, Dict
from app.services.customer_service import get_consolidated_customers

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get(
    "/consolidated",
    response_model=List[Dict],
    summary="Consultar datos financieros consolidados",
    description="""
Este endpoint permite validar que los archivos CSV se han leído correctamente.

""",
    response_description="Listado de clientes con su información financiera"
)
def get_all_customers():
    """
    Devuelve una lista de diccionarios con la información consolidada de los clientes, incluyendo préstamos, tarjetas y otros datos financieros.
    """
    return get_consolidated_customers()
