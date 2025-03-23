from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import asyncio
from contextlib import asynccontextmanager
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict
import os
from dotenv import load_dotenv
from enum import Enum
from sqlalchemy import select, and_, or_
import logging

from database import get_db, engine
import models
from email_service import EmailService

# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Define task status enum
class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Background task for sending reminders
async def check_reminders():
    """Background task to check for tasks with upcoming reminders and send notifications."""
    while True:
        try:
            db = next(get_db())
            try:
                # Get tasks with reminders due in the next hour
                now = datetime.utcnow()
                one_hour_from_now = now + timedelta(hours=1)
                
                # Query for tasks that:
                # 1. Have a deadline in the next hour
                # 2. Haven't been completed
                # 3. Haven't had a reminder sent in the last day
                tasks = db.query(models.Task).join(models.User).filter(
                    and_(
                        models.Task.deadline >= now,
                        models.Task.deadline <= one_hour_from_now,
                        models.Task.status != TaskStatus.COMPLETED,
                        or_(
                            models.Task.last_reminder.is_(None),
                            models.Task.last_reminder <= now - timedelta(days=1)
                        )
                    )
                ).all()
                
                for task in tasks:
                    # Get the task owner
                    owner = task.owner
                    
                    if owner and owner.email:
                        # Send reminder email
                        email_service = EmailService()
                        success = await email_service.send_reminder(task, owner.email)
                        
                        if success:
                            # Update last_reminder timestamp
                            task.last_reminder = now
                            db.commit()
            finally:
                db.close()
                
        except Exception as e:
            logging.error(f"Error in reminder check task: {str(e)}")
        
        # Wait for 15 minutes before checking again
        await asyncio.sleep(900)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create background task
    reminder_task = asyncio.create_task(check_reminders())
    yield
    # Shutdown: Cancel background task
    reminder_task.cancel()
    try:
        await reminder_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

# CORS middleware - update with frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Default for development
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALLOWED_EMAIL = "epiphanywanjira@gmail.com"  # Your email address

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Root route to serve index.html
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("static/index.html")

# Pydantic models
class TaskBase(BaseModel):
    title: str
    description: str
    deadline: datetime
    reminder_time: datetime
    status: TaskStatus = TaskStatus.NOT_STARTED
    week_number: Optional[int] = None
    phase: Optional[str] = None
    tools_resources: Optional[str] = None
    notes: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int
    last_reminder: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if the email is allowed
        if user.email != ALLOWED_EMAIL:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Registration is restricted to authorized users only"
            )

        # Check if user already exists
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Registration error: {str(e)}")
        db.rollback()
        raise

@app.post("/tasks/", response_model=Task)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        db_task = models.Task(**task.model_dump(), owner_id=current_user.id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create task")

@app.get("/tasks/", response_model=List[Task])
async def read_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
        return tasks
    except Exception as e:
        logging.error(f"Error fetching tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch tasks")

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_update: TaskBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        db_task = db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.owner_id == current_user.id
        ).first()
        
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        for key, value in task_update.model_dump().items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not update task")

@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        db_task = db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.owner_id == current_user.id
        ).first()
        
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(db_task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not delete task") 