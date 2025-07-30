from fastapi import APIRouter
from app.services.customer_service import get_consolidated_customers

router = APIRouter()

@router.get("/consolidated")
def get_all_customers():
    return get_consolidated_customers()

