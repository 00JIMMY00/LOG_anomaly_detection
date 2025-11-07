from fastapi import APIRouter, HTTPException, status
from typing import Dict
import logging

from app.models import LogRequest, LogResponse, HealthResponse
from app.controllers import LogController

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["logs"]
)

# Initialize controller
log_controller = LogController()


@router.post(
    "/analyze",
    response_model=LogResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze a log message",
    description="Analyze a log message and determine if it's an anomaly or normal"
)
async def analyze_log(request: LogRequest) -> LogResponse:
    """
    Analyze a log message for anomalies.
    
    - **log_message**: The log message to analyze
    - **threshold**: Optional confidence threshold (0.0 to 1.0, default: 0.5)
    
    Returns classification result with label, confidence, and anomaly status.
    """
    try:
        return log_controller.analyze_log(request)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while analyzing the log message"
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the health status of the API and model"
)
async def health_check() -> HealthResponse:
    """
    Check the health status of the API.
    
    Returns the status of the API and whether the model is loaded.
    """
    return log_controller.get_health()


@router.get(
    "/",
    response_model=Dict[str, str],
    summary="API root",
    description="Get basic API information"
)
async def root() -> Dict[str, str]:
    """
    Root endpoint providing basic API information.
    """
    return {
        "message": "Log Anomaly Detection API",
        "version": "1.0.0",
        "docs": "/docs"
    }
