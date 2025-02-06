from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from database import get_db
from models import User, Prediction, PatientInfo, DoctorInfo
from utils.image_processing import preprocess_image
import os
import numpy as np
import tensorflow as tf

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MODEL_PATH = "tensorflow_model/Alzhemier_model_CNN_latest.h5"
alzheimers_model = None
alzheimers_model = tf.keras.models.load_model(MODEL_PATH)

@router.post("/", response_model=dict)
def predict(file: UploadFile, patientID: int = Form(...), doctorID: int= Form(...), api_key: str= Form(...), db: Session = Depends(get_db)):
    global alzheimers_model

    if alzheimers_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Contact admin.")

    # Validate user API key
    user = db.exec(select(User).where(User.api_key == api_key)).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Validate patient and doctor IDs
    patient = db.exec(select(PatientInfo).where(PatientInfo.patientID == patientID)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    doctor = db.exec(select(DoctorInfo).where(DoctorInfo.doctorID == doctorID)).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Preprocess the image
        image_array = preprocess_image(file_path, target_size=(128, 128))  # Resize to 128x128
        image_array = np.expand_dims(image_array, axis=0) / 255.0  # Normalize

        # Run inference using the loaded model
        predictions = alzheimers_model.predict(image_array)
        predicted_class = int(np.argmax(predictions[0]))  # Ensure it's a Python int
        confidence_score = float(predictions[0][predicted_class])  # Ensure it's a Python float

        prediction_label = [
            "Mild Demented",
            "Moderate Demented",
            "Non-Demented",
            "Very Mild Demented"
        ][predicted_class]

        # Save prediction to the database
        new_prediction = Prediction(
            user_id=user.id,
            patientID=patientID,
            doctorID=doctorID,
            image_path=file_path,
            prediction=prediction_label,
            timestamp=datetime.utcnow()
        )
        db.add(new_prediction)
        db.commit()

        return {"result": prediction_label, "confidence": confidence_score}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
