import os
import importlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config.base import Base
from pathlib import Path

DB_FOLDER = "output"
DB_NAME = "products.db"
db_path = os.path.join(DB_FOLDER, DB_NAME)

# Create connection and session globally
engine = create_engine(f"sqlite:///{db_path}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_db():
    """Table creator."""
    os.makedirs(DB_FOLDER, exist_ok=True)

    models_directory = Path(__file__).parent / "models"

    # Dynamically imports all models
    for filename in models_directory.glob("*.py"):
        if filename.name != "__init__.py":
            module_name = f"database.models.{filename.stem}"
            try:
                importlib.import_module(module_name)
            except ModuleNotFoundError:
                print(f"Error importing module {module_name}. Make sure it's properly configured.")

    # Create the tables
    Base.metadata.create_all(engine)

def get_db():
    """
    Session generator
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
