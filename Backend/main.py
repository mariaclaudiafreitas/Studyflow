from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users, subjects, tasks
# Create tables
Base.metadata.create_all(bind=engine)
app = FastAPI(title="StudyFlow API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only, update for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(subjects.router)
app.include_router(tasks.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to StudyFlow API"}
