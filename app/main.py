from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import router
from app.db import database as d
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Fix: Allow all methods
    allow_headers=["*"],  # Fix: Allow all headers
)

# Include routes
app.include_router(router.router, prefix="/cases", tags=["Cases"])

async def check_connection():
    try:
        await d.command("ping")
        print("✅ MongoDB is connected!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(check_connection())  # Fix: Runs without blocking

@app.get("/")
async def root():
    return {"message": "Welcome to the Case Management API"}
