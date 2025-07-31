# 💼 BCP Challenge - Análisis y Consolidación Financiera

Este proyecto es una API desarrollada con **FastAPI** que realiza análisis financieros para clientes. A través de datos como préstamos, tarjetas, historial crediticio y flujo de caja, genera escenarios y recomendaciones utilizando **IA generativa**.

## 🚀 Tecnologías

- Python 3.10+
- FastAPI
- Azure Blob Storage (lectura de archivos)
- OpenAI GPT (Azure OpenAI Service)
- Pandas

---

## 📦 Requisitos

- Python 3.10 o superior
- `pip`
- Cuenta de Azure (con acceso a Blob Storage y OpenAI)
- Git
- OpenAI API Key y Endpoint

---

## 🛠️ Instalación y ejecución local

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/bcpchallenge.git
cd bcpchallenge
```

### 2. Crea un entorno virtual

```bash
python -m venv .venv
```

### 3. Activa el entorno virtual

- En Windows:

```bash
.venv\Scripts\activate
```

- En macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Instala dependencias

```bash
pip install -r requirements.txt
```

### 5. Configura las variables de entorno

Crea un archivo `.env` en la raíz del proyecto y añade lo siguiente:

```env
# Azure Blob Storage
AZURE_BLOB_BASE_URL=

# OpenAI
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT_NAME=
AZURE_OPENAI_API_VERSION=

```

> Puedes generar el token SAS desde el portal de Azure en tu contenedor.

---

## ▶️ Ejecución local

Una vez configurado todo:

```bash
uvicorn app.main:app --reload
```

Abre tu navegador en:  
📍 http://127.0.0.1:8000/docs

---

## 📬 Ejemplo de uso en Postman

Endpoint: `POST /api/conversation`  
URL: `http://127.0.0.1:8000/api/conversation`

Body (JSON):

```json
{
  "message": "Quiero un análisis financiero",
  "session_id": "session_id"
}
```

---

## 📁 Estructura del Proyecto

```
bcpchallenge/
│
├── app/
│   ├── main.py                # Config principal de FastAPI
│   ├── routes/                # Endpoints de la API
│   ├── services/              # Lógica de negocio
│   ├── prompts/               # Prompts de IA generativa
│   └── ...
│
├── .env                       # Variables de entorno (no subir al repo)
├── requirements.txt           # Dependencias del proyecto
└── README.md
```

---
