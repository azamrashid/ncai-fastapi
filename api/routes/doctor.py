from fastapi import APIRouter, Depends, Form,HTTPException
from sqlmodel import Session, select
from database import get_db
from models import DoctorInfo
from schemas import DoctorCreate

router = APIRouter()

@router.post("/", response_model=DoctorInfo)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = DoctorInfo(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

# Route for all Doctors Data
@router.get("/", response_model=list[DoctorInfo])
def get_doctors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.exec(select(DoctorInfo).offset(skip).limit(limit)).all()

# Route for Specific DoctorID
@router.get("/{doctorID}", response_model=DoctorInfo)
def get_doctor(doctorID: int, db: Session = Depends(get_db)):
    # Query the database for the specific doctor
    doctor = db.exec(select(DoctorInfo).where(DoctorInfo.doctorID == doctorID)).first()
    
    # If the doctor is not found, raise a 404 error
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return doctor