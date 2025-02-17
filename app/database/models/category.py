from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.config.base import Base


class Category(Base):
    """
    Represents a product category in the database.
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
