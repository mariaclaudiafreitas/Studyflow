from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import Base,get_db
router = APIRouter(prefix="/subjects", tags=["subjects"])
@router.post("/", response_model=schemas.SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_subject = models.Subject(**subject.dict(), user_id=current_user.id)
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject
@router.get("/", response_model=List[schemas.SubjectResponse])
def get_subjects(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Subject).filter(models.Subject.user_id == current_user.id).all()
@router.put("/{subject_id}", response_model=schemas.SubjectResponse)
def update_subject(subject_id: int, subject: schemas.SubjectUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id, models.Subject.user_id == current_user.id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
        
    for key, value in subject.dict().items():
        setattr(db_subject, key, value)
        
    db.commit()
    db.refresh(db_subject)
    return db_subject
@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id, models.Subject.user_id == current_user.id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
        
    db.delete(db_subject)
    db.commit()
    return {"message": "Subject deleted successfully"}
