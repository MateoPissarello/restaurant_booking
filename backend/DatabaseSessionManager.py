from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables or use a default value
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"  # noqa


class DatabaseSessionManager:
    """
    Singleton class to manage the SQLAlchemy database session.

    This class ensures that only one instance of the database session manager exists
    throughout the application's lifetime. It provides a global point of access
    to the database session, simplifying database interactions.
    """

    _instance = None  # Class-level variable to hold the single instance

    def __new__(cls, *args, **kwargs):
        """
        Overrides the default __new__ method to implement the singleton pattern.

        If an instance of the class doesn't exist, it creates one and stores it
        in the `_instance` variable. Otherwise, it returns the existing instance.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, db_url: str = DATABASE_URL):
        """
        Initializes the database session manager.

        This method is called only once, when the singleton instance is created.
        It sets up the database engine, session maker, and base for declarative models.

        Args:
            db_url (str, optional): The database connection URL.
                Defaults to the value from environment variables.
        """
        if not hasattr(self, "_initialized"):  # Prevent re-initialization
            self.engine = create_engine(db_url, echo=True)  # Consider echo=False in production
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.Base = declarative_base()
            self._initialized = True

    def get_db(self) -> Generator[Session, None, None]:
        """
        Provides a database session.  This is intended to be used as a
        dependency in FastAPI.

        Yields:
            Session: An SQLAlchemy database session.

        Example Usage:
        ```python
        from fastapi import Depends, FastAPI
        from sqlalchemy.orm import Session
        from your_module import DatabaseSessionManager  # Import the singleton

        app = FastAPI()
        db_manager = DatabaseSessionManager() # Get the instance

        def get_db(): # Your dependency
            yield db_manager.get_db()

        @app.get("/items/")
        async def read_items(db: Session = Depends(get_db)):
            # Use the database session here
            items = db.query(YourModel).all()
            return items
        ```
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_all_tables(self):
        """
        Creates all tables defined in the application's models.

        This method should be called once during application startup.
        It uses the `Base` from the singleton instance to create the tables.
        """
        self.Base.metadata.create_all(bind=self.engine)

    @classmethod
    def get_instance(cls) -> "DatabaseSessionManager":
        """
        Class method to get the singleton instance.

        Returns:
            DatabaseSessionManager: The singleton instance of the class.
        """
        if not cls._instance:
            cls._instance = cls()  # Create the instance if it doesn't exist
        return cls._instance


# Usage (replace original get_db function)
db_manager = DatabaseSessionManager()  # Get the instance of the singleton


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get a database session.

    This function uses the singleton instance of DatabaseSessionManager to
    retrieve a database session.
    """
    yield from db_manager.get_db()  # Use the generator from the instance
