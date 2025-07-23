from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)


@router.post("/", response_model=schemas.ArticleOut)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    article_data = article.model_dump()
    article_data.pop('topics', None)  

    db_article = models.Article(**article_data, author_id=current_user.id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    topic_objects = []
    for topic_title in article.topics:
        topic = db.query(models.Topic).filter(
            models.Topic.title.ilike(topic_title)
        ).first()

        if not topic:
            topic = models.Topic(title=topic_title)
            db.add(topic)
            db.flush()  
        topic_objects.append(topic)

    db_article.topic = topic_objects
    db.commit()
    db.refresh(db_article)

    return db_article


@router.get("/user/{user_id}", response_model=list[schemas.ArticleOut])
def get_user_articles(user_id: int, db: Session = Depends(get_db)):
    articles = db.query(models.Article).filter(
        models.Article.author_id == user_id).all()
    return articles


@router.get("/{article_id}", response_model=schemas.ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(
        models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article

@router.patch("/{article_id}", response_model=schemas.ArticleOut)
def update_article(article_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db_article = db.query(models.Article).filter(
        models.Article.id == article_id, models.Article.author_id == current_user.id).first()
    
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found or you do not have permission to edit it")

    article_data = article.model_dump()
    article_data.pop('topics', None)

    for key, value in article_data.items():
        setattr(db_article, key, value)

    topic_objects = []
    for topic_title in article.topics:
        topic = db.query(models.Topic).filter(
            models.Topic.title.ilike(topic_title)
        ).first()

        if not topic:
            topic = models.Topic(title=topic_title)
            db.add(topic)
            db.flush()  
        topic_objects.append(topic)

    db_article.topic = topic_objects

    db.commit()
    db.refresh(db_article)
    return db_article


@router.post("/{article_id}/like", status_code=status.HTTP_201_CREATED)
def like_article(article_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(
        models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    if current_user in article.liked_by:
        article.liked_by.remove(current_user)
        db.commit()
        db.refresh(article)
        return {"message": "Article unliked successfully"}
    else:
        article.liked_by.append(current_user)
        db.commit()
        db.refresh(article)
        return {"message": "Article liked successfully"}

@router.post("/{article_id}/comment", status_code=status.HTTP_201_CREATED)
def comment_on_article(article_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(
        models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    new_comment = models.Comment(
        **comment.model_dump(), article_id=article.id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.post("/{article_id}/comment/{comment_id}/reply", status_code=status.HTTP_201_CREATED)
def reply_to_comment(article_id: int, comment_id: int, reply: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(
        models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    parent_comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id, models.Comment.article_id == article.id).first()
    if not parent_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    new_reply = models.Comment(**reply.model_dump(), article_id=article.id,
                               user_id=current_user.id, parent_id=parent_comment.id)
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


@router.get("/search", status_code=status.HTTP_200_OK)
def global_search(search_string: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not search_string:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Search string cannot be empty")
    
    search_string = f"%{search_string}%"

    articles = db.query(
        models.Article.title.ilike(search_string), models.Article.is_published == True, models.Article.subtitle.ilike(search_string)).all()

    users = db.query(models.User.username.ilike(search_string)).all()

    topics = db.query(models.Topic.title.ilike(search_string), models.Topic.articles.filter(models.Article.is_published == True)).all()

    return {
        "articles": articles,
        "users": users,
        "topics": topics
    }