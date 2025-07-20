from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AuthUserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")

    try:
        user.password = utils.hash(user.password)

        # Create user in the database
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = oauth2.create_access_token(
            data={"user_id": new_user.id})

        return {"access_token": access_token, "token_type": "bearer",   "id": new_user.id,
                "email": new_user.email,
                "username": new_user.username,
                "created_at": new_user.created_at}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while creating the user: {str(e)}")


@router.get("/", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(
        models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    user_query = db.query(models.User).filter(
        models.User.id == current_user.id)
    existing_user = user_query.first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = user.model_dump(exclude_unset=True, exclude_none=True)

    if update_data:
        user_query.update(update_data, synchronize_session=False)
        db.commit()

    return user_query.first()


@router.put("/add_topics", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
def update_user_topics(
    topics_data: schemas.TopicCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    user = db.query(models.User).filter(
        models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    existing_titles = {t.title.lower() for t in user.interested_topics}
    new_topics = []
    for topic in topics_data.topics:
        if topic.lower() not in existing_titles:
            existing_topic = db.query(models.Topic).filter(
                models.Topic.title.ilike(topic)).first()
            if not existing_topic:
                existing_topic = models.Topic(title=topic)
                db.add(existing_topic)
                db.flush()  
            new_topics.append(existing_topic)
    user.interested_topics.extend(new_topics)

    db.commit()
    db.refresh(user)
    return user


@router.get("/feeds", response_model=list[schemas.ArticleOut])
def get_user_feeds(
    current_user: int = Depends(oauth2.get_current_user)
):
    feeds = []
    for topic in current_user.interested_topics:
        feeds.extend(topic.articles)

    return feeds

@router.get("/dashboard", response_model=schemas.UserDashboard)
def get_user_dashboard(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    user = db.query(models.User).filter(
        models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    dashboard_data = schemas.UserDashboard(
        id=user.id,
        email=user.email,
        username=user.username,
        topics=user.interested_topics,
        articles=user.articles,
            articles_count=len(user.articles),
            followers_count=len(user.followers),
            following_count=len(user.following),
            followers=user.followers,
            following=user.following,
            twitter_url=user.twitter_url,
            instagram_url=user.instagram_url,
            website_url=user.website_url,
            youtube_url=user.youtube_url,
            linkedin_url=user.linkedin_url,
            github_url=user.github_url,
            location=user.location,
            profile_image=user.profile_image,
            bio=user.bio
        )

    return dashboard_data


@router.get("/{id}", response_model=schemas.UserDashboard)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
