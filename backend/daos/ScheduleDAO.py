from sqlalchemy.orm import Session
from models import Schedule
from datetime import time
from datetime import date as dt
from typing import List
from models import days


class ScheduleDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_schedule(self, schedule_id: int) -> Schedule | None:
        schedule = self.db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()
        return schedule

    def create_schedule(self, schedule: Schedule) -> Schedule:
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        return schedule

    def get_schedule_by_restaurant(self, restaurant_id: int) -> List[Schedule]:
        schedule = self.db.query(Schedule).filter(Schedule.restaurant_id == restaurant_id).all()
        return schedule

    def update_schedule(self, schedule_id: int, updated_data: dict) -> Schedule | None:
        schedule = self.get_schedule(schedule_id)
        if schedule:
            for key, value in updated_data.items():
                setattr(schedule, key, value)
            self.db.commit()
            self.db.refresh(schedule)
            return schedule
        return None

    def delete_schedule(self, schedule_id: int) -> bool:
        restaurant_id = self.get_schedule(schedule_id)
        if restaurant_id:
            self.db.delete(restaurant_id)
            self.db.commit()
            return True
        return False

    def is_restaurant_open(self, restaurant_id: int, date: dt, start_hour: time, end_hour: time) -> bool:
        weekday_str = date.strftime("%A").lower()

        try:
            reservation_day = days(weekday_str)
        except ValueError:
            raise ValueError(f"Invalid day: {weekday_str}. Must be one of {', '.join(day.name for day in days)}")

        schedule = (
            self.db.query(Schedule)
            .filter(
                Schedule.restaurant_id == restaurant_id,
                Schedule.day.in_([reservation_day, days.all]),  # Acepta horario específico o 'all'
                Schedule.opening_hour <= start_hour,
                Schedule.closing_hour >= end_hour,
            )
            .first()
        )
        return schedule is not None
