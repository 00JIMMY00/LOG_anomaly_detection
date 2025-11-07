import os
from transformers import pipeline
from typing import Dict, Optional
import logging

from app.config import MODEL_DIR, MODEL_NAME, CLASSIFICATION_LABELS

logger = logging.getLogger(__name__)


class ModelService:
    """Service class for handling model loading and inference"""
    
    _instance = None
    _pipeline = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one model instance"""
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
        return cls._instance
    
    def load_model(self, force_reload: bool = False) -> bool:
        """
        Load the zero-shot classification model from local directory.
        
        Args:
            force_reload: Force reload the model even if already loaded
            
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        if self._pipeline is not None and not force_reload:
            logger.info("Model already loaded")
            return True
        
        try:
            # Check if model exists locally
            if not os.path.exists(MODEL_DIR):
                logger.error(f"Model directory not found: {MODEL_DIR}")
                logger.info("Please run 'python download_model.py' to download the model first")
                return False
            
            logger.info(f"Loading model from {MODEL_DIR}")
            self._pipeline = pipeline(
                "zero-shot-classification",
                model=str(MODEL_DIR)
            )
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._pipeline is not None
    
    def inference(self, log_message: str, threshold: float = 0.5) -> Dict:
        """
        Perform inference on a log message to detect anomalies.
        
        Args:
            log_message: The log message to classify
            threshold: Confidence threshold for classification (default: 0.5)
        
        Returns:
            dict: {
                'label': str,
                'confidence': float,
                'is_anomaly': bool,
                'scores': dict
            }
        """
        if self._pipeline is None:
            raise RuntimeError("Model not loaded. Please load the model first.")
        
        try:
            # Perform zero-shot classification
            result = self._pipeline(log_message, candidate_labels=CLASSIFICATION_LABELS)
            
            # Get the predicted label and its confidence
            predicted_label = result['labels'][0]
            confidence = result['scores'][0]
            
            # Apply threshold logic
            if confidence >= threshold:
                final_label = predicted_label
                final_confidence = confidence
            else:
                # If confidence is below threshold, return the other label
                final_label = result['labels'][1]
                final_confidence = result['scores'][1]
            
            # Create scores dictionary
            scores = {
                label: score 
                for label, score in zip(result['labels'], result['scores'])
            }
            
            return {
                'label': final_label,
                'confidence': float(final_confidence),
                'is_anomaly': final_label == 'anomaly',
                'scores': scores
            }
            
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            'model_loaded': self.is_loaded(),
            'model_path': str(MODEL_DIR),
            'model_name': MODEL_NAME
        }
