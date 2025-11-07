from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from app.routers import router
from app.services import ModelService
from app.config import API_TITLE, API_VERSION, API_DESCRIPTION

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler to load the model on application start.
    """
    logger.info("Starting Log Anomaly Detection API...")
    
    model_service = ModelService()
    success = model_service.load_model()
    
    if success:
        logger.info("Model loaded successfully on startup")
    else:
        logger.warning(
            "Model not loaded on startup. "
            "Please run 'python download_model.py' to download the model."
        )


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler for cleanup.
    """
    logger.info("Shutting down Log Anomaly Detection API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
