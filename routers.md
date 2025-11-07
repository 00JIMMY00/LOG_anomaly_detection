# API Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## Overview
The Log Anomaly Detection API provides endpoints for analyzing log messages using a zero-shot classification model to detect anomalies.

---

## Endpoints

### 1. Root Endpoint

**GET** `/api/v1/`

Returns basic API information.

#### Response
```json
{
  "message": "Log Anomaly Detection API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

#### Example cURL
```bash
curl -X GET "http://localhost:8000/api/v1/"
```

---

### 2. Analyze Log Message

**POST** `/api/v1/analyze`

Analyzes a log message and determines if it's an anomaly or normal.

#### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `log_message` | string | Yes | The log message to analyze |
| `threshold` | float | No | Confidence threshold (0.0-1.0, default: 0.5) |

#### Request Example
```json
{
  "log_message": "request body exceeds the configured limit, client=55.213.84.244",
  "threshold": 0.5
}
```

#### Response
| Field | Type | Description |
|-------|------|-------------|
| `log_message` | string | The original log message |
| `label` | string | Classification label: 'anomaly' or 'normal' |
| `confidence` | float | Confidence score of the prediction (0.0-1.0) |
| `is_anomaly` | boolean | True if the log is classified as an anomaly |
| `threshold` | float | The threshold used for classification |

#### Response Example
```json
{
  "log_message": "request body exceeds the configured limit, client=55.213.84.244",
  "label": "anomaly",
  "confidence": 0.9945,
  "is_anomaly": true,
  "threshold": 0.5
}
```

#### Status Codes
- `200 OK` - Successfully analyzed the log
- `503 Service Unavailable` - Model not loaded
- `500 Internal Server Error` - An error occurred during analysis

#### Example cURL
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "log_message": "request body exceeds the configured limit, client=55.213.84.244",
    "threshold": 0.5
  }'
```

#### Example Python
```python
import requests

url = "http://localhost:8000/api/v1/analyze"
payload = {
    "log_message": "request body exceeds the configured limit, client=55.213.84.244",
    "threshold": 0.5
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Label: {result['label']}")
print(f"Confidence: {result['confidence']}")
print(f"Is Anomaly: {result['is_anomaly']}")
```

---

### 3. Health Check

**GET** `/api/v1/health`

Checks the health status of the API and whether the model is loaded.

#### Response
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "/path/to/models/deberta-v3-base-zeroshot"
}
```

#### Status Codes
- `200 OK` - Health check successful

#### Example cURL
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Classification Logic

The API uses a zero-shot classification model to analyze log messages:

1. The log message is processed by the DeBERTa model
2. The model assigns confidence scores for both "anomaly" and "normal" labels
3. The label with the highest confidence is selected as the primary prediction
4. If the confidence is below the threshold, the secondary label is returned instead
5. The response includes the final label, confidence score, and a boolean flag indicating if it's an anomaly

### Threshold Behavior

- **threshold >= 0.5**: More conservative, requires high confidence to classify as anomaly
- **threshold < 0.5**: More sensitive, easier to classify as anomaly
- **Default**: 0.5

---

## Error Handling

The API returns appropriate HTTP status codes and error messages:

### Model Not Loaded (503)
```json
{
  "detail": "Model not loaded. Please load the model first."
}
```

### Internal Server Error (500)
```json
{
  "detail": "An error occurred while analyzing the log message"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "log_message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Usage Examples

### Example 1: Detecting an Anomaly
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "log_message": "ERROR: Database connection timeout after 30s"
  }'
```

### Example 2: Normal Log
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "log_message": "User login successful, session_id=abc123"
  }'
```

### Example 3: Custom Threshold
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "log_message": "Warning: High memory usage at 85%",
    "threshold": 0.7
  }'
```

---

## Notes

- The model must be downloaded first using `python download_model.py`
- The API loads the model on startup
- All timestamps in logs are in UTC
- The API supports CORS for cross-origin requests
