from sqlalchemy.orm import Session
from models import Restaurant


class RestaurantDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_restaurant(self, restaurant_id: int) -> Restaurant | None:
        restaurant = self.db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
        return restaurant

    def create_restaurant(self, resturant: Restaurant) -> Restaurant:
        self.db.add(resturant)
        self.db.commit()
        self.db.refresh(resturant)
        return resturant

    def list_restaurants(self) -> list[Restaurant]:
        restaurants = self.db.query(Restaurant).all()
        return restaurants

    def update_restaurant(self, restaurant_id: int, updated_data: dict) -> Restaurant | None:
        restaurant = self.get_restaurant(restaurant_id)
        if restaurant:
            for key, value in updated_data.items():
                setattr(restaurant, key, value)
            self.db.commit()
            self.db.refresh(restaurant)
            return restaurant
        return None

    def get_restaurant_by_name(self, name: str) -> Restaurant | None:
        restaurant = self.db.query(Restaurant).filter(Restaurant.name == name).first()
        return restaurant

    def delete_restaurant(self, restaurant_id: int) -> bool:
        restaurant_id = self.get_restaurant(restaurant_id)
        if restaurant_id:
            self.db.delete(restaurant_id)
            self.db.commit()
            return True
        return False
