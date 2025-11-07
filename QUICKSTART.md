# Quick Start Guide

## Setup and Run in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download the Model
```bash
python download_model.py
```
This will download the model (~1.5 GB) and save it to `models/deberta-v3-base-zeroshot/`

### Step 3: Start the API Server
```bash
python app/main.py
```
or
```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

---

## Test the API

### 1. Check Health
```bash
curl http://localhost:8000/api/v1/health
```

### 2. Analyze a Log (Anomaly)
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "log_message": "ERROR: Database connection timeout after 30s"
  }'
```

Expected response:
```json
{
  "log_message": "ERROR: Database connection timeout after 30s",
  "label": "anomaly",
  "confidence": 0.98,
  "is_anomaly": true,
  "threshold": 0.5
}
```

### 3. Analyze a Log (Normal)
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "log_message": "User login successful, session created"
  }'
```

---

## Access Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Python Client Example

```python
import requests

# Analyze a log
url = "http://localhost:8000/api/v1/analyze"
response = requests.post(url, json={
    "log_message": "request body exceeds the configured limit",
    "threshold": 0.5
})

result = response.json()
print(f"Is Anomaly: {result['is_anomaly']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

## Project Structure

```
LOG_anomaly_detection/
├── app/                          # FastAPI application
│   ├── main.py                   # Entry point
│   ├── config.py                 # Configuration
│   ├── models/                   # Pydantic schemas
│   │   └── schemas.py
│   ├── controllers/              # Business logic
│   │   └── log_controller.py
│   ├── services/                 # Model service
│   │   └── model_service.py
│   └── routers/                  # API routes
│       └── log_router.py
├── models/                       # Stored ML model (created after download)
│   └── deberta-v3-base-zeroshot/
├── download_model.py             # Model download script
├── requirements.txt              # Dependencies
├── routers.md                    # API documentation
├── BACKEND_README.md             # Detailed backend docs
└── QUICKSTART.md                 # This file
```

---

## Need Help?

- See `routers.md` for detailed API documentation
- See `BACKEND_README.md` for comprehensive backend information
- Visit http://localhost:8000/docs for interactive API docs
