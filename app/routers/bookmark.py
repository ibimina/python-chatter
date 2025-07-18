from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/bookmarks",
    tags=["bookmarks"]
)

@router.get("/", response_model=list[schemas.ArticleOut])
def get_bookmarked_articles(db: Session = Depends(get_db), current_user: int = Depends
(oauth2.get_current_user)):
    
    articles = db.query(models.Article).filter(models.Article.bookmarked_by.any(id=current_user.id)).all()
    return articles

@router.post("/{article_id}", status_code=status.HTTP_201_CREATED)
def bookmark_article(article_id: int, db: Session = Depends(get_db), current_user:
int = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    if current_user in article.bookmarked_by:
        article.bookmarked_by.remove(current_user)
        db.commit()
        db.refresh(article)
        return {"message": "Article removed from bookmarks"}

    article.bookmarked_by.append(current_user)
    db.commit()
    db.refresh(article)
    return {"message": "Article bookmarked successfully"}