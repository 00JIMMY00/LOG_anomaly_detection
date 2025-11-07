#!/usr/bin/env python3
"""
Script to download and save the zero-shot classification model locally.
Run this script before starting the FastAPI server.
"""

import os
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Model configuration
MODEL_NAME = "MoritzLaurer/deberta-v3-base-zeroshot-v2.0"
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models" / "deberta-v3-base-zeroshot"


def download_model():
    """
    Download the model and tokenizer from Hugging Face and save them locally.
    """
    try:
        logger.info(f"Starting model download: {MODEL_NAME}")
        logger.info(f"Target directory: {MODEL_DIR}")
        
        # Create model directory if it doesn't exist
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        
        # Check if model already exists
        if (MODEL_DIR / "config.json").exists():
            logger.warning("Model already exists in the directory.")
            response = input("Do you want to re-download? (y/n): ")
            if response.lower() != 'y':
                logger.info("Skipping download.")
                return True
        
        logger.info("Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        tokenizer.save_pretrained(MODEL_DIR)
        logger.info("✓ Tokenizer downloaded and saved")
        
        logger.info("Downloading model (this may take several minutes)...")
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        model.save_pretrained(MODEL_DIR)
        logger.info("✓ Model downloaded and saved")
        
        logger.info(f"\n✓ Model successfully downloaded to: {MODEL_DIR}")
        logger.info("\nYou can now start the FastAPI server with:")
        logger.info("  python -m uvicorn app.main:app --reload")
        logger.info("or")
        logger.info("  python app/main.py")
        
        return True
        
    except Exception as e:
        logger.error(f"Error downloading model: {str(e)}")
        logger.error("\nPlease check your internet connection and try again.")
        return False


def verify_model():
    """
    Verify that the model files exist.
    """
    required_files = ["config.json", "pytorch_model.bin", "tokenizer_config.json"]
    missing_files = []
    
    for file in required_files:
        if not (MODEL_DIR / file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.warning(f"Missing files: {', '.join(missing_files)}")
        return False
    
    logger.info("✓ All required model files are present")
    return True


def main():
    """
    Main function to download and verify the model.
    """
    logger.info("=" * 60)
    logger.info("Log Anomaly Detection Model Download")
    logger.info("=" * 60)
    
    success = download_model()
    
    if success:
        logger.info("\nVerifying model files...")
        verify_model()
        logger.info("\n✓ Setup complete!")
    else:
        logger.error("\n✗ Setup failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
