from typing import List, Optional
from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from models import Base, TaskModel, Task, TaskCreate
from db import engine, get_db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(
    prefix="/api",
    tags=["tasks"]  # Tag for documentation purposes
)

# Create the table if it's new
Base.metadata.create_all(bind=engine)

# ====
# APIs
# ====

@api_router.get("/")
def get_index():
    return {"message": "Benvenuto in Tudù! Visita la pagina /docs per la documentazione!"}


@api_router.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
async def get_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task con ID {task_id} non trovato."
        )
    return task


@api_router.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
async def get_tasks(completed: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter(TaskModel.completed == completed)
    return query.all()


@api_router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    if len(task_in.title.strip()) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Il titolo deve essere lungo massimo 200 caratteri."
        )
    new_task = TaskModel(
        id=str(uuid4()),
        title=task_in.title,
        description=task_in.description,
        completed=task_in.completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@api_router.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
async def update_task(task_id: UUID, task_update: TaskCreate, db: Session = Depends(get_db)):
    if len(task_update.title.strip()) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Il titolo deve essere lungo massimo 200 caratteri."
        )
    task_query = db.query(TaskModel).filter(TaskModel.id == str(task_id))
    db_task = task_query.first()
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task con ID {task_id} non trovato."
        )
    task_query.update(task_update.dict(), synchronize_session=False)
    db.commit()
    db.refresh(db_task)
    return db_task


@api_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    task_query = db.query(TaskModel).filter(TaskModel.id == str(task_id))
    db_task = task_query.first()
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task con ID {task_id} non trovato."
        )
    task_query.delete(synchronize_session=False)
    db.commit()
    return


app.include_router(api_router)
