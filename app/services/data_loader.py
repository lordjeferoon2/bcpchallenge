import pandas as pd
import json
from azure.storage.blob import BlobServiceClient, ContainerClient
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

# Carga variables desde .env
load_dotenv()

CONTAINER_SAS_URL = os.getenv("AZURE_BLOB_BASE_URL")

def load_all_data():
    try:
        # Usa la URL completa del contenedor con el token SAS
        container_client = ContainerClient.from_container_url(CONTAINER_SAS_URL)
        
        # Nombres de los archivos
        files = {
            "loans": "loan.csv",
            "cards": "cards.csv",
            "payments": "payments_history.csv",
            "scores": "credit_score_history.csv",
            "cashflows": "customer_cashflow.csv",
        }
        
        data = {}

        # Leer archivos CSV
        for key, filename in files.items():
            blob_client = container_client.get_blob_client(filename)
            blob_data = blob_client.download_blob().readall()
            df = pd.read_csv(pd.io.common.BytesIO(blob_data))
            data[key] = df.to_dict(orient="records")
        
        # Leer archivo JSON
        offers_blob_client = container_client.get_blob_client("bank_offers.json")
        offers_data = offers_blob_client.download_blob().readall()
        data["offers"] = json.loads(offers_data)

        return data
    
    except Exception as e:
        print(f"Error al conectar con Azure Blob Storage usando SAS: {e}")
        return None