# Log Anomaly Detection System

A production-ready **FastAPI backend** for detecting anomalies in log messages using zero-shot classification with the DeBERTa-v3 model. This system provides a RESTful API to analyze log messages and classify them as **anomaly** or **normal** with confidence scores.

## 🎯 What is This Project?

This project is an **AI-powered log analysis system** that:

- 🔍 **Analyzes log messages** in real-time via REST API
- 🤖 Uses **zero-shot classification** (no training required)
- 📊 Returns **confidence scores** and anomaly detection results
- 🏗️ Built with **FastAPI** following **MVC architecture**
- 💾 Stores the model **locally** (no repeated downloads)
- 📝 Provides **interactive API documentation** (Swagger UI)

### Use Cases

- **System Monitoring**: Detect unusual patterns in application logs
- **Security Analysis**: Identify potential security threats in access logs
- **DevOps**: Automate log analysis in CI/CD pipelines
- **Incident Response**: Quickly classify log entries during troubleshooting

## 🏗️ Architecture

The project follows **MVC (Model-View-Controller)** architecture:

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── models/              # Pydantic schemas (data models)
├── controllers/         # Business logic layer
├── services/            # Model inference service
└── routers/             # API route definitions
```

## 📋 Prerequisites

- **Python 3.8+** (Python 3.10 recommended)
- **4GB+ RAM** (model requires ~2-3GB in memory)
- **~2GB disk space** (for model files)
- **Internet connection** (for initial model download)

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd LOG_anomaly_detection

# Install all required packages
pip install -r requirements.txt
```

### Step 2: Download the Model

**IMPORTANT**: You must download the model before starting the API server.

```bash
python download_model.py
```

This downloads the DeBERTa model (~1.5GB) and saves it to `models/deberta-v3-base-zeroshot/`

### Step 3: Start the API Server

```bash
# Option 1: Using the main script
python app/main.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **API is now running at**: http://localhost:8000

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/v1/analyze` | Analyze a log message and detect anomalies |
| **GET** | `/api/v1/health` | Check API health and model status |
| **GET** | `/api/v1/` | Get API information |
| **GET** | `/docs` | Interactive API documentation (Swagger UI) |
| **GET** | `/redoc` | Alternative API documentation (ReDoc) |

### 1. Analyze Log Message

**Endpoint**: `POST /api/v1/analyze`

**Request Body**:
```json
{
  "log_message": "ERROR: Database connection timeout after 30s",
  "threshold": 0.5
}
```

**Response**:
```json
{
  "log_message": "ERROR: Database connection timeout after 30s",
  "label": "anomaly",
  "confidence": 0.9876,
  "is_anomaly": true,
  "threshold": 0.5
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "log_message": "request body exceeds the configured limit",
    "threshold": 0.5
  }'
```

**Python Example**:
```python
import requests

url = "http://localhost:8000/api/v1/analyze"
payload = {
    "log_message": "ERROR: Database connection timeout",
    "threshold": 0.5
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Is Anomaly: {result['is_anomaly']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### 2. Health Check

**Endpoint**: `GET /api/v1/health`

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "/path/to/models/deberta-v3-base-zeroshot"
}
```

**cURL Example**:
```bash
curl http://localhost:8000/api/v1/health
```

### 3. API Root

**Endpoint**: `GET /api/v1/`

**Response**:
```json
{
  "message": "Log Anomaly Detection API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

## 📖 Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API testing and complete documentation.

## 🔧 Configuration

### Threshold Parameter

The `threshold` parameter controls classification sensitivity:

- **0.3-0.5**: More sensitive, catches more anomalies (may have false positives)
- **0.5** (default): Balanced approach
- **0.7-0.9**: More conservative, fewer false positives (may miss some anomalies)

### Model Configuration

Edit `app/config.py` to customize:

```python
MODEL_NAME = "MoritzLaurer/deberta-v3-base-zeroshot-v2.0"
MODEL_DIR = BASE_DIR / "models" / "deberta-v3-base-zeroshot"
DEFAULT_THRESHOLD = 0.5
CLASSIFICATION_LABELS = ["anomaly", "normal"]
```

## 📓 Jupyter Notebook (Alternative)

For interactive exploration, use the Jupyter notebook:

```bash
jupyter notebook inference.ipynb
```

The notebook provides a simple `inference()` function:

```python
result = inference("your log message here", threshold=0.5)
print(f"Label: {result['label']}, Confidence: {result['confidence']:.4f}")
```

## 📊 Dataset

The dataset (`dataset/LOG_dataset.xlsx`) contains log entries from:

- [LogHub](https://github.com/logpai/loghub) - Comprehensive log datasets
- [CloudOps BERT](https://huggingface.co/vaibhav2507/cloudops-bertto) - Cloud operations logs

## 🤖 Model Information

- **Model**: DeBERTa-v3-base-zeroshot-v2.0
- **Architecture**: Zero-shot classification with DeBERTa
- **Task**: Binary classification (anomaly vs. normal)
- **Size**: ~1.5GB
- **Source**: [Hugging Face Model Hub](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0)
- **Storage**: Saved locally in `models/` directory

## 🛠️ Project Structure

```
LOG_anomaly_detection/
├── app/                          # FastAPI application
│   ├── main.py                   # Application entry point
│   ├── config.py                 # Configuration settings
│   ├── models/                   # Pydantic schemas
│   │   └── schemas.py
│   ├── controllers/              # Business logic
│   │   └── log_controller.py
│   ├── services/                 # Model service
│   │   └── model_service.py
│   └── routers/                  # API routes
│       └── log_router.py
├── models/                       # Stored ML model (after download)
│   └── deberta-v3-base-zeroshot/
├── dataset/                      # Training/testing datasets
│   └── LOG_dataset.xlsx
├── download_model.py             # Model download script
├── inference.ipynb               # Jupyter notebook for testing
├── requirements.txt              # Python dependencies
├── routers.md                    # Detailed API documentation
├── BACKEND_README.md             # Backend-specific documentation
├── QUICKSTART.md                 # Quick start guide
└── mermaid_diagrams.md           # System architecture diagrams
```

## 🚨 Troubleshooting

### "Model not loaded" Error (503)

**Problem**: API returns 503 Service Unavailable

**Solution**: Download the model first
```bash
python download_model.py
```

### Port Already in Use

**Problem**: Port 8000 is already occupied

**Solution**: Use a different port
```bash
uvicorn app.main:app --port 8001
```

### Import Errors

**Problem**: Module not found errors

**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Model Download Fails

**Problem**: Network issues during download

**Solution**: 
1. Check internet connection
2. Try again - the script will resume if partially downloaded
3. Manually download from [Hugging Face](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0)

## 📚 Additional Documentation

- **`routers.md`** - Complete API endpoint documentation with examples
- **`BACKEND_README.md`** - Detailed backend architecture and development guide
- **`QUICKSTART.md`** - Quick setup and testing guide
- **`mermaid_diagrams.md`** - System architecture diagrams (use case, sequence, DFD, etc.)

## 💻 Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --log-level debug
```

### Adding New Endpoints

1. Define schema in `app/models/schemas.py`
2. Add business logic in `app/controllers/`
3. Create route in `app/routers/`
4. Include router in `app/main.py`

## 🔒 Security Notes

- CORS is enabled for all origins (modify for production)
- No authentication implemented (add JWT/OAuth if needed)
- Input validation via Pydantic models
- Consider rate limiting for production deployments

## 📈 Performance

- **First Request**: ~500-1000ms (model initialization)
- **Subsequent Requests**: ~100-500ms per log
- **Memory Usage**: ~2-3GB RAM for model
- **Concurrent Requests**: Handled efficiently by FastAPI async

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows MVC architecture
- API endpoints are documented
- Tests are included for new features

## 📄 License

This project uses the DeBERTa model which is licensed under MIT License.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `routers.md` for API documentation
3. Check `BACKEND_README.md` for backend details
4. Open an issue on the repository

---

**Made with ❤️ using FastAPI and Transformers**
