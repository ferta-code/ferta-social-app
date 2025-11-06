from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import PostingSchedule
from app.schemas import PostingScheduleResponse, PostingScheduleCreate

router = APIRouter()


@router.get("/", response_model=List[PostingScheduleResponse])
def get_schedules(db: Session = Depends(get_db)):
    """Get all posting schedules"""
    schedules = db.query(PostingSchedule).all()
    return schedules


@router.post("/", response_model=PostingScheduleResponse)
def create_schedule(schedule: PostingScheduleCreate, db: Session = Depends(get_db)):
    """Create a new posting schedule"""
    db_schedule = PostingSchedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Delete a posting schedule"""
    schedule = db.query(PostingSchedule).filter(PostingSchedule.id == schedule_id).first()
    if not schedule:
        return {"message": "Schedule not found"}

    db.delete(schedule)
    db.commit()
    return {"message": "Schedule deleted successfully"}
