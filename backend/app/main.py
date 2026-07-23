from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.routers import auth
from app.routers import palm

# Import models so SQLAlchemy knows about them
from app.model import user
from app.model import palm_analysis
from app.model import palm_interpretation
from app.model.tarot_card import TarotCard
from app.routers import tarot
from app.model.user import User
from app.model.palm_analysis import PalmAnalysis
from app.model.tarot_reading import TarotReading
from app.routers import reports
from app.model.three_card_reading import ThreeCardReading

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Palmistry & Tarot Intelligence Platform"
)


# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Authentication routes
app.include_router(auth.router)


# Palm analysis routes
app.include_router(palm.router)
app.include_router(tarot.router)
app.include_router(reports.router)


@app.get("/")
def home():

    return {
        "message": "API Running Successfully"
    }