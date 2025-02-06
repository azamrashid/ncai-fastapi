from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    api_key: Optional[str] = Field(default=None, unique=True)

class PatientInfo(SQLModel, table=True):
    patientID: Optional[int] = Field(default=None, primary_key=True)
    patientName: str
    patientAge: int
    patient_Decease: str
    checkup_Date: datetime
    doctorID: int = Field(foreign_key="doctorinfo.doctorID")
    patient_EntryDateTime: datetime = Field(default_factory=datetime.utcnow)

class DoctorInfo(SQLModel, table=True):
    doctorID: Optional[int] = Field(default=None, primary_key=True)
    doctor_Name: str
    doctor_Specialisation: str
    doctor_EntryDateTime: datetime = Field(default_factory=datetime.utcnow)

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    patientID: int = Field(foreign_key="patientinfo.patientID")
    doctorID: int = Field(foreign_key="doctorinfo.doctorID")
    image_path: str
    prediction: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)