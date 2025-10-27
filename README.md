# Log Anomaly Detection

A zero-shot classification system for detecting anomalies in log messages using the DeBERTa-v3 model. This project leverages state-of-the-art transformer models to identify abnormal patterns in system logs without requiring extensive training data.

## 🎯 Overview

This project uses the pre-trained [MoritzLaurer/deberta-v3-base-zeroshot-v2.0](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0) model for zero-shot classification of log messages. The model can distinguish between normal and anomalous log entries with high accuracy.

## 📋 Prerequisites

- Python 3.8 or higher
- Anaconda or Miniconda installed on your system
- 4GB+ RAM recommended
- GPU support optional (CPU inference supported)

## 🚀 Setup Instructions

### 1. Create Anaconda Environment

```bash
# Create a new conda environment
conda create -n log_anomaly python=3.10 -y

# Activate the environment
conda activate log_anomaly
```

### 2. Install Dependencies

```bash
# Navigate to the project directory
cd /path/to/LOG_anomaly_detection

# Install required packages
pip install -r requirements.txt
```

## 📓 Using the Inference Notebook

### Opening the Notebook

1. After launching Jupyter, navigate to `inference.ipynb` in the browser
2. Ensure your kernel is set to the `log_anomaly` environment
3. Run all cells sequentially

### Running Inference

The notebook provides a simple `inference()` function:

```python
# Basic usage
result = inference("your log message here")
print(f"Label: {result['label']}, Confidence: {result['confidence']:.4f}")

# With custom threshold
result = inference("your log message here", threshold=0.7)
```

**Parameters:**

- `log_message` (str): The log message to classify
- `threshold` (float, optional): Confidence threshold (default: 0.5)

**Returns:**

- Dictionary with `label` (anomaly/normal) and `confidence` score

### Example Usage

```python
# Example 1: Anomalous log
log1 = "request body exceeds the configured limit, client=55.213.84.244"
result1 = inference(log1)
# Output: {'label': 'anomaly', 'confidence': 0.9945}

# Example 2: Normal log
log2 = "User login successful, session started"
result2 = inference(log2)
# Output: {'label': 'normal', 'confidence': 0.8523}
```

## 📊 Dataset

The dataset (`dataset/LOG_dataset.xlsx`) contains log entries collected from multiple sources:

- [LogHub](https://github.com/logpai/loghub) - Comprehensive log datasets
- [CloudOps BERT](https://huggingface.co/vaibhav2507/cloudops-bertto) - Modern cloud operations logs

## 🔧 Model Information

- **Model**: DeBERTa-v3-base-zeroshot-v2.0
- **Architecture**: Zero-shot classification
- **Task**: Binary classification (anomaly vs. normal)
- **Source**: [Hugging Face Model Hub](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0)

## 💡 Tips

- **First Run**: The model will be downloaded automatically (~1.5GB). This may take a few minutes.
- **Threshold Tuning**: Adjust the threshold parameter based on your use case:

  - Lower threshold (0.3-0.5): More sensitive, catches more anomalies
  - Higher threshold (0.7-0.9): More conservative, fewer false positives
- **Batch Processing**: For multiple logs, iterate through your dataset and call `inference()` for each entry
