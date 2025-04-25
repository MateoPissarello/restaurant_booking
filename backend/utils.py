from database import DBSession
from sqlalchemy.orm import Session
from fastapi import Depends


def get_db(db: Session = Depends(DBSession.get_db)):
    return db
