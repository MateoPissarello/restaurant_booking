from sqlalchemy.orm import Session
from daos.RestaurantDAO import RestaurantDAO


def validate_restaurant_existence(restaurant_id: int, db: Session) -> bool:
    """
    Validate if a restaurant exists in the database.

    Args:
        restaurant_id (int): The ID of the restaurant to validate.
        db (Session): The database session.

    Returns:
        bool: True if the restaurant exists, False otherwise.
    """

    dao = RestaurantDAO(db)
    restaurant = dao.get_restaurant(restaurant_id)
    return restaurant is not None
