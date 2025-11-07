from typing import Dict
import logging

from app.services import ModelService
from app.models import LogRequest, LogResponse, HealthResponse
from app.config import DEFAULT_THRESHOLD

logger = logging.getLogger(__name__)


class LogController:
    """Controller for handling log analysis requests"""
    
    def __init__(self):
        self.model_service = ModelService()
    
    def analyze_log(self, request: LogRequest) -> LogResponse:
        """
        Analyze a log message for anomalies.
        
        Args:
            request: LogRequest containing log message and optional threshold
            
        Returns:
            LogResponse with analysis results
        """
        # Use provided threshold or default
        threshold = request.threshold if request.threshold is not None else DEFAULT_THRESHOLD
        
        try:
            # Perform inference
            result = self.model_service.inference(
                log_message=request.log_message,
                threshold=threshold
            )
            
            # Create response
            response = LogResponse(
                log_message=request.log_message,
                label=result['label'],
                confidence=result['confidence'],
                is_anomaly=result['is_anomaly'],
                threshold=threshold
            )
            
            logger.info(
                f"Analyzed log: label={result['label']}, "
                f"confidence={result['confidence']:.4f}, "
                f"is_anomaly={result['is_anomaly']}"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error analyzing log: {str(e)}")
            raise
    
    def get_health(self) -> HealthResponse:
        """
        Get API health status.
        
        Returns:
            HealthResponse with health information
        """
        model_info = self.model_service.get_model_info()
        
        return HealthResponse(
            status="healthy" if model_info['model_loaded'] else "unhealthy",
            model_loaded=model_info['model_loaded'],
            model_path=model_info['model_path']
        )
