from sqlalchemy import Column, String, Float, Boolean, Index, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database.config.base import Base


class Product(Base):
    """
    Represents a product in the database.
    """

    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    sale_price = Column(Float)
    image_url = Column(String)
    in_stock = Column(Boolean, nullable=False, default=True)
    source_url = Column(String)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")

    __table_args__ = (
        Index("idx_price_name", "price", "name"),  
        Index("idx_category_id", "category_id"),  
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "sale_price": self.sale_price,
            "image_url": self.image_url,
            "in_stock": self.in_stock,
            "source_url": self.source_url,
            "category": self.category.name if self.category else "Unavailable",
            "category_id": self.category_id,
        }
