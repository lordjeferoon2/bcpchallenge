from fastapi import FastAPI
from app.routes import conversation, customers
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Customer Consolidation API")

# Permitir CORS para Angular local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Puedes usar ["*"] en desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos como "GET", "POST"
    allow_headers=["*"],  # Headers permitidos
)

# Incluir rutas
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(conversation.router, prefix="/api")
