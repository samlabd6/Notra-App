# FastAPI backend for Personal Knowledge Notes API
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm

from fastapi import FastAPI, HTTPException, Depends
# SQLAlchemy imports for database interaction
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
# Local imports for database setup, models, schemas, and encryption
from database import get_db, engine
from tables import Base, Note, User
from schemas import NoteCreate, NoteResponse, UserCreate, UserLogin, UserResponse, Token 
from encryp import hash_password, verify_password
from oauth import create_access_token, verify_access_token, get_current_user, get_current_active_user




app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/notices", response_model=list[NoteResponse])
def get_all_posts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    WHERE = Note.user_id == current_user.id
    return db.query(Note).filter(WHERE).all() 

@app.get("/notices/{id}", response_model=NoteResponse)
def get_post(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db) ):
    notice = db.get(Note, id)
    WHERE = Note.user_id == id and Note.user_id == current_user.id
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice


@app.post("/notices", response_model=NoteResponse)                 
def create_notice(notice: NoteCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    new_note = Note(**notice.model_dump())
    new_note.user_id = current_user.id
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/posts/{id}") 
def update_post(id: int):
    pass

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    notice = db.get(Note, id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    db.delete(notice)
    db.commit()
    return {"message": "Notice deleted successfully"}


@app.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_pw[1], salt=hashed_pw[0])
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")

# Login endpoint is now handled by the /token route using OAuth2PasswordRequestForm, so we can remove the old login endpoint
#@app.post("/login", response_model=UserResponse)
#def login(user: UserLogin, db: Session = Depends(get_db)):
#    db_user = db.query(User).filter(User.username == user.username).first() 
#    
#    if not db_user or not verify_password(db_user.salt, db_user.password_hash, user.password):
#        raise HTTPException(status_code=401, detail="Invalid username or password")
#    
#    return db_user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(user.salt, user.password_hash, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}