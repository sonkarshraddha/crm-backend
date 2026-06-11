from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base
from routes.tickets import router
import os

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Serve frontend folder
app.mount("/frontend_", StaticFiles(directory="frontend_"), name="frontend")


# Open frontend automatically
@app.get("/")
def home():
    return FileResponse("frontend_/index.html")


# Health check
@app.get("/api")
def api_home():
    return {
        "message": "Customer Support CRM API Running"
    }