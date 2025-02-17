from database.models.category import Category
from database.models.product import Product
from database.db import get_db
from sqlalchemy import desc

def get_all_products():
    db = next(get_db())
    try:
        return [
            product.to_dict() 
            for product in db.query(Product)
            .order_by(Product.category_id, desc(Product.price), Product.name)
            .all()
        ]
    finally:
        db.close()


def save_product(product_data, db):
    existing_product = db.query(Product).filter_by(name=product_data["name"]).first()

    if existing_product:
        for key, value in product_data.items():
            if value is not None:
                setattr(existing_product, key, value)
    else:
        new_product = Product(**product_data)
        db.add(new_product)

    db.commit()


def get_or_create_category(db, category_name):
    existing_category = db.query(Category).filter_by(name=category_name).first()
    if not existing_category:
        new_category = Category(name=category_name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category.id
    return existing_category.id
