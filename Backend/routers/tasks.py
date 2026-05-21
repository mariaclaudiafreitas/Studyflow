from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import Base, get_db
router = APIRouter(prefix="/tasks", tags=["tasks"])
def _chunk_task_if_needed(task: schemas.TaskCreate, db: Session, current_user: models.User) -> List[models.Task]:
    """
    Simulação da IA: Heurística que divide tarefas grandes em blocos menores.
    Se a tarefa tem mais de 120 minutos, divide em blocos de 60 minutos.
    """
    if task.estimated_minutes and task.estimated_minutes > 120:
        created_tasks = []
        num_chunks = task.estimated_minutes // 60
        remainder = task.estimated_minutes % 60
        
        for i in range(num_chunks):
            chunk_task = models.Task(
                title=f"{task.title} (Parte {i+1}) - Sugestão IA",
                description=task.description,
                estimated_minutes=60,
                subject_id=task.subject_id,
                user_id=current_user.id,
                is_ai_suggested=True
            )
            db.add(chunk_task)
            created_tasks.append(chunk_task)
            
        if remainder > 0:
            final_task = models.Task(
                title=f"{task.title} (Parte Final) - Sugestão IA",
                description=task.description,
                estimated_minutes=remainder,
                subject_id=task.subject_id,
                user_id=current_user.id,
                is_ai_suggested=True
            )
            db.add(final_task)
            created_tasks.append(final_task)
            
        return created_tasks
    else:
        # Tarefa normal
        normal_task = models.Task(**task.dict(), user_id=current_user.id)
        db.add(normal_task)
        return [normal_task]
@router.post("/", response_model=List[schemas.TaskResponse], status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Valida se subject existe e pertence ao user
    if task.subject_id:
        subject = db.query(models.Subject).filter(models.Subject.id == task.subject_id, models.Subject.user_id == current_user.id).first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found or does not belong to user")
            
    # Aplica lógica de IA simulada (heurística de chunking)
    created_tasks = _chunk_task_if_needed(task, db, current_user)
    db.commit()
    for t in created_tasks:
        db.refresh(t)
        
    return created_tasks
@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}