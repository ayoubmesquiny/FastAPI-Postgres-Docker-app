from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import items  
from app.core.db import create_db_connection
from app.core.config import settings 

app = FastAPI(title=settings.PROJECT_NAME)

# Optional: Configure CORS (if you're working with frontend applications or other services)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, but you can restrict it to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods like GET, POST, PUT, DELETE
    allow_headers=["*"],  # Allows all headers
)

app.include_router(items.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    await create_db_connection()

@app.on_event("shutdown")
async def shutdown():
    pass
