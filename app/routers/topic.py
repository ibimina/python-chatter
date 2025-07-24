from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)

@router.get("/", response_model=list[schemas.TopicOut])
def get_all_topics(db: Session = Depends(get_db)):
    topics = db.query(models.Topic).all()
    return topics

@router.get("/{topic_title}", response_model=schemas.TopicOut)
def get_topic_by_title(topic_title: str, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.title.ilike(topic_title)).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("/", response_model=schemas.TopicOut)
def create_topic(topic: schemas.SingleTopic, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(
    models.User.id == current_user.id)
    existing_user = user_query.first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    topic_query = db.query(models.Topic).filter(models.Topic.title.ilike(f"%{topic.topic}%"))
    existing_topic = topic_query.first()
    if existing_topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic already exist")


    new_topic = models.Topic(title=topic.topic)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

@router.post("/follow/{topic_id}", status_code=status.HTTP_201_CREATED)
def topic_following(topic_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    existing_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not existing_topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    
    if current_user in existing_topic.interested_users:
        existing_topic.interested_users.remove(current_user)
        db.commit()
        message = f"Unfollowed topic '{existing_topic.title}'"
    else:
        existing_topic.interested_users.append(current_user)
        db.commit()
        message = f"Following topic '{existing_topic.title}'"

    return {"message": message}
