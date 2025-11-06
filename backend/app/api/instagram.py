from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import InstagramPost
from app.schemas import InstagramPostResponse, InstagramPostCreate, InstagramPostUpdate

router = APIRouter()


@router.get("/", response_model=List[InstagramPostResponse])
def get_instagram_posts(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all Instagram posts, optionally filtered by status"""
    query = db.query(InstagramPost)
    if status:
        query = query.filter(InstagramPost.status == status)
    posts = query.order_by(InstagramPost.created_at.desc()).offset(skip).limit(limit).all()
    return posts


@router.get("/{post_id}", response_model=InstagramPostResponse)
def get_instagram_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific Instagram post by ID"""
    post = db.query(InstagramPost).filter(InstagramPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Instagram post not found")
    return post


@router.post("/", response_model=InstagramPostResponse)
def create_instagram_post(post: InstagramPostCreate, db: Session = Depends(get_db)):
    """Create a new Instagram post"""
    db_post = InstagramPost(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.patch("/{post_id}", response_model=InstagramPostResponse)
def update_instagram_post(
    post_id: int,
    post_update: InstagramPostUpdate,
    db: Session = Depends(get_db)
):
    """Update an Instagram post"""
    post = db.query(InstagramPost).filter(InstagramPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Instagram post not found")

    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}")
def delete_instagram_post(post_id: int, db: Session = Depends(get_db)):
    """Delete an Instagram post"""
    post = db.query(InstagramPost).filter(InstagramPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Instagram post not found")

    db.delete(post)
    db.commit()
    return {"message": "Instagram post deleted successfully"}
