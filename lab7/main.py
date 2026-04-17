from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from typing import List

from database import get_db, Task, init_db
from models import TaskCreate, TaskUpdate, TaskResponse
from security import (
    limiter, security_headers_middleware, 
    create_access_token, get_current_user, 
    Token, oauth2_scheme, get_password_hash, verify_password
)

app = FastAPI(
    title="Task Manager API (Secure)",
    description="REST API с механизмами безопасности",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(security_headers_middleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", tags=["System"])
@limiter.limit("10/minute")
def root(request: Request):
    return {"message": "Secure Task Manager API", "docs": "/docs"}

@app.post("/auth/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
@limiter.limit("5/minute")
async def register(request: Request, username: str, password: str, db: Session = Depends(get_db)):
    hashed = get_password_hash(password)
    return {"message": f"User {username} registered"}

@app.post("/auth/token", response_model=Token, tags=["Auth"])
@limiter.limit("10/minute")
async def login(request: Request, username: str, password: str, db: Session = Depends(get_db)):
    if username != "admin" or not verify_password(password, get_password_hash("admin123")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
@limiter.limit("30/minute")
def create_task(
    request: Request,
    task: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Требуется токен
):
    db_task = Task(**task.model_dump(), owner=current_user)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[TaskResponse], tags=["Tasks"])
@limiter.limit("60/minute")
def list_tasks(
    request: Request,
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(Task).offset(skip).limit(limit).all()

# ... остальные CRUD-методы аналогично с добавлением Depends(get_current_user)

@app.get("/security-check", tags=["System"])
@limiter.limit("5/minute")
def security_check(request: Request):
    return {
        "message": "Security headers applied",
        "note": "Check response headers in browser devtools or Postman"
    }