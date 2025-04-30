from sqlalchemy.orm import Session
from models import User


class UserDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> User | None:
        user = self.db.query(User).filter(User.user_id == user_id).first()
        return user

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_users(self) -> list[User]:
        users = self.db.query(User).all()
        return users

    def update_user(self, user_id: int, updated_data: dict) -> User | None:
        user = self.get_user(user_id)
        if user:
            for key, value in updated_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            return user

    def delete_user(self, user_id: int) -> bool:
        user_id = self.get_user(user_id)
        if user_id:
            self.db.delete(user_id)
            self.db.commit()
            return True
        return False
