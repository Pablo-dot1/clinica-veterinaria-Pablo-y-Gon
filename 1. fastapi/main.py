from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database import engine
import db_models

# Create database tables
db_models.Base.metadata.create_all(bind=engine)

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

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Veterinary Clinic API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        workers=1,  # Limitar a un solo worker
        reload=False  # Deshabilitar auto-reload
    )
