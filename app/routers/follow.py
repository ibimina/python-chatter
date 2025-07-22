from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/follow",
    tags=["follow"]
)

@router.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def follow_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")
    
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if current_user in target_user.followers:
            target_user.followers.remove(current_user)
            db.commit()
            return {"message": f"You are not following {target_user.username}"}
    else: 
        target_user.followers.append(current_user)
        db.commit()
        return {"message": f"You are now following {target_user.username}"}

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if current_user not in target_user.followers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not following this user")
    
    target_user.followers.remove(current_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/users/{user_id}/followers", response_model=list[schemas.UserOut])
def get_user_followers(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user.followers

@router.get("/users/{user_id}/following", response_model=list[schemas.UserOut])
def get_user_following(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user.following

@router.get("/me/followers", response_model=list[schemas.UserOut])
def get_my_followers(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    return current_user.followers

@router.get("/me/following", response_model=list[schemas.UserOut])
def get_my_following(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    return current_user.following

@router.get("/users/{user_id}/status")
def check_follow_status(
    user_id: int,
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    is_following = current_user in target_user.followers
    return {
        "is_following": is_following,
        "follower_count": len(target_user.followers),
        "following_count": len(target_user.following)
    }

@router.get("/suggestions", response_model=list[schemas.UserOut])
def get_follow_suggestions(
    limit: int = 10,
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    following_ids = [user.id for user in current_user.following]
    following_ids.append(current_user.id)  
    
    suggestions = db.query(models.User).filter(
        ~models.User.id.in_(following_ids)
    ).limit(limit).all()
    
    return suggestions