# Log Anomaly Detection API - Backend

A FastAPI-based backend service for detecting anomalies in log messages using zero-shot classification with DeBERTa model.

## Architecture

The project follows **MVC (Model-View-Controller)** architecture:

```
app/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── models/                # Pydantic models (schemas)
│   ├── __init__.py
│   └── schemas.py
├── controllers/           # Business logic layer
│   ├── __init__.py
│   └── log_controller.py
├── services/              # Service layer (model inference)
│   ├── __init__.py
│   └── model_service.py
└── routers/               # API routes
    ├── __init__.py
    └── log_router.py
```

## Features

- **Zero-shot classification** for log anomaly detection
- **RESTful API** with FastAPI
- **MVC architecture** for clean code organization
- **Local model storage** (no repeated downloads)
- **Automatic model loading** on startup
- **Interactive API documentation** (Swagger UI)
- **Health check endpoint**
- **Configurable confidence threshold**

## Prerequisites

- Python 3.8+
- pip

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the model:**
   ```bash
   python download_model.py
   ```
   
   This will download the `MoritzLaurer/deberta-v3-base-zeroshot-v2.0` model and save it locally in the `models/` directory (~1.5 GB).

## Running the API

### Option 1: Using uvicorn directly
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Using the main script
```bash
python app/main.py
```

### Option 3: Using Python module syntax
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Endpoints Documentation**: See `routers.md`

## Quick Start Example

### 1. Check API Health
```bash
curl http://localhost:8000/api/v1/health
```

### 2. Analyze a Log Message
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "log_message": "ERROR: Database connection timeout after 30s",
    "threshold": 0.5
  }'
```

Response:
```json
{
  "log_message": "ERROR: Database connection timeout after 30s",
  "label": "anomaly",
  "confidence": 0.9876,
  "is_anomaly": true,
  "threshold": 0.5
}
```

### 3. Using Python Requests
```python
import requests

url = "http://localhost:8000/api/v1/analyze"
payload = {
    "log_message": "User login successful",
    "threshold": 0.5
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Label: {result['label']}")
print(f"Confidence: {result['confidence']:.4f}")
print(f"Is Anomaly: {result['is_anomaly']}")
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/` | API root information |
| POST | `/api/v1/analyze` | Analyze log message |
| GET | `/api/v1/health` | Health check |
| GET | `/docs` | Swagger UI documentation |
| GET | `/redoc` | ReDoc documentation |

## Configuration

Edit `app/config.py` to customize:

- `MODEL_DIR`: Directory where model is stored
- `DEFAULT_THRESHOLD`: Default confidence threshold (0.5)
- `CLASSIFICATION_LABELS`: Labels for classification
- API metadata (title, version, description)

## Project Structure Details

### Models (Schemas)
- `LogRequest`: Input schema for log analysis
- `LogResponse`: Output schema with classification results
- `HealthResponse`: Health check response schema

### Services
- `ModelService`: Singleton service for model loading and inference
  - Loads model from local directory
  - Performs zero-shot classification
  - Caches model in memory

### Controllers
- `LogController`: Business logic for log analysis
  - Validates requests
  - Calls model service
  - Formats responses

### Routers
- `log_router`: API route definitions
  - `/analyze` endpoint for log classification
  - `/health` endpoint for system status

## How It Works

1. **Model Loading**: On startup, the API loads the DeBERTa model from the local `models/` directory
2. **Request Processing**: Log message is received via POST request
3. **Zero-Shot Classification**: Model classifies log as "anomaly" or "normal"
4. **Threshold Application**: Confidence score is compared against threshold
5. **Response**: Returns label, confidence, and boolean anomaly flag

## Troubleshooting

### Model not loaded error
```bash
# Download the model first
python download_model.py
```

### Port already in use
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Development

### Adding New Endpoints

1. Define schema in `app/models/schemas.py`
2. Add business logic in `app/controllers/`
3. Create route in `app/routers/`
4. Include router in `app/main.py`

### Testing

```bash
# Run the server
python app/main.py

# In another terminal, test endpoints
curl http://localhost:8000/api/v1/health
```

## Performance Considerations

- **First Request**: May be slower as model initializes
- **Subsequent Requests**: Fast inference (~100-500ms per log)
- **Memory Usage**: ~2-3 GB RAM for model
- **Concurrent Requests**: FastAPI handles async requests efficiently

## Security Notes

- CORS is enabled for all origins (modify in production)
- No authentication implemented (add if needed)
- Input validation via Pydantic models
- Consider rate limiting for production use

## License

Same as parent project.

## Support

For issues or questions, refer to `routers.md` for detailed API documentation.
