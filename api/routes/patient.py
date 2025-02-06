from fastapi import APIRouter, Depends, Form, HTTPException
from sqlmodel import Session, select
from database import get_db
from models import PatientInfo
from schemas import PatientCreate

router = APIRouter()

@router.post("/", response_model=PatientInfo)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = PatientInfo(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@router.get("/", response_model=list[PatientInfo])
def get_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.exec(select(PatientInfo).offset(skip).limit(limit)).all()

@router.get("/{patientID}", response_model=PatientInfo)
def get_patient(patientID: int, db: Session = Depends(get_db)):
    # Query the database for the specific patient
    patient = db.exec(select(PatientInfo).where(PatientInfo.patientID == patientID)).first()
    
    # If the patient is not found, raise a 404 error
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient