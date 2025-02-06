from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, prediction, patient, doctor
from database import create_db_and_tables
import tensorflow as tf
import os

app = FastAPI(title="NeuroCogni AI ML/DL Models Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific domains like ["http://localhost:3000"] for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load the TensorFlow model on startup
MODEL_PATH = "tensorflow_model/Alzhemier_model_CNN_latest.h5"
alzheimers_model = None

@app.on_event("startup")
async def on_startup():
    global alzheimers_model
    if os.path.exists(MODEL_PATH):
        alzheimers_model = tf.keras.models.load_model(MODEL_PATH)
        print("TensorFlow model loaded successfully.")
    else:
        print("Model file not found at", MODEL_PATH)
    create_db_and_tables()

@app.get("/")
async def health_check():
    return "The health check is successful!"

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(prediction.router, prefix="/predict", tags=["Prediction"])
app.include_router(patient.router, prefix="/patients", tags=["Patient Management"])
app.include_router(doctor.router, prefix="/doctors", tags=["Doctor Management"])
