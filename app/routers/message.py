from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

@router.get("/", response_model=list[schemas.MessageOut])
def get_user_messages (db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    messages = db.query(models.Message).filter(
        (models.Message.sender_id == current_user.id) | 
        (models.Message.receiver_id == current_user.id)
    ).all()
    return messages

@router.get("/{user_id}", response_model=list[schemas.MessageOut])
def get_messages_with_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == user_id)) |
         ((models.Message.sender_id == user_id) & (models.Message.receiver_id == current_user.id))
    ).all()
    return messages

@router.post("/{user_id}", response_model=schemas.MessageOut)
def send_message(user_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot send a message to yourself")

    new_message = models.Message(**message.model_dump(), sender_id=current_user.id, receiver_id=user_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
