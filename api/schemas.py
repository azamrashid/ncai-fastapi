from sqlmodel import SQLModel
from datetime import datetime

class PatientCreate(SQLModel):
    patientName: str
    patientAge: int
    patient_Decease: str
    checkup_Date: datetime
    doctorID: int

class DoctorCreate(SQLModel):
    doctor_Name: str
    doctor_Specialisation: str

class PredictionCreate(SQLModel):
    patientID: int
    doctorID: int
    image_path: str
    prediction: str

class PredictionResponse(SQLModel):
    id: int
    patientID: int
    doctorID: int
    image_path: str
    prediction: str
    timestamp: datetime

class UserCreate(SQLModel):
    email: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str