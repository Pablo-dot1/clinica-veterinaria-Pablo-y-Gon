from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import router
from database import engine, check_database_connection
import db_models
import logging
import sys
import psutil
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create database tables
try:
    db_models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {str(e)}")
    raise

app = FastAPI(
    title="Veterinary Clinic API",
    description="API for managing a veterinary clinic",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Verify connections and dependencies at startup"""
    logger.info("Starting application...")
    try:
        check_database_connection()
        logger.info("Database connection verified")
    except Exception as e:
        logger.error(f"Error during application startup: {str(e)}")
        raise

@app.get("/")
async def root():
    try:
        return {
            "message": "Welcome to the Veterinary Clinic API",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    try:
        # Check database connection
        check_database_connection()
        
        # Get system information
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "healthy",
            "database": "connected",
            "system_info": {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "disk_usage": f"{disk.percent}%",
                "memory_available": f"{memory.available/1024/1024:.2f} MB",
                "disk_available": f"{disk.free/1024/1024:.2f} MB"
            }
        }
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "detail": str(e),
                "service": "API"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
