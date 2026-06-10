from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.tickets import router

app = FastAPI()

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

@app.on_event("startup")
def startup():
    # safer place to create tables
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Customer Support CRM API Running"}