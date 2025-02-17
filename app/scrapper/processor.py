from core.db_helper import get_or_create_category, save_product
from core.constants import BASE_URL
from urllib.parse import urljoin
from database.db import get_db


import re


def parse_product_page(response):
    db = next(get_db())
    product_id = response.url.split("/")[-1]
    if not product_id.isdigit():
        return

    title = response.css(".title::text").get(default="N/A").strip()
    description = response.css(".description::text").get(default="N/A").strip()
    price_text = response.css(".price::text").get(default="N/A").strip()
    price_value = extract_price(price_text)

    availability_text = (
        response.css(".availability::text").get(default="Out of stock").strip()
    )
    is_in_stock = availability_text.lower() == "in stock"

    images = response.css("img")
    new_images = [
        img
        for img in images
        if img.attrib.get("alt") == title and img.attrib.get("srcset")
    ]
    url_image = extract_image(new_images[0]) if new_images else None

    product_data = {
        "id": product_id,
        "name": title,
        "description": description,
        "price": price_value,
        "sale_price": price_value,
        "in_stock": is_in_stock,
        "image_url": url_image,
        "source_url": response.url,
    }

    save_product(product_data, db)
    db.close()


def parse_category_page(response):
    db = next(get_db())

    category_id = None

    if "category" in response.url:
        parts = response.url.split("category", 1)
        if len(parts) > 1:
            url_path = parts[1].split("?", 1)[0]
            categories = [cat for cat in url_path.split("/") if cat]

            if categories:
                category_id = get_or_create_category(db, categories[0])

    cards = response.css(".product-card")
    for card in cards:
        link = card.css("a::attr(href)").get()
        if link:
            id = link.split("/")[-1]
            title = card.css(".title::text").get(default="N/A").strip()
            price_text = card.css(".price-wrapper::text").get(default="N/A").strip()
            price_value = extract_price(price_text)
            description = card.css(".description::text").get(default="N/A").strip()

            product_data = {
                "id": id,
                "name": title,
                "description": description,
                "price": price_value,
                "sale_price": price_value,
                "category_id": category_id,
            }

            save_product(product_data, db)

    db.close()


def extract_price(price_str):
    """Extract a floating-point value from a price string."""
    match = re.search(r"[\d.,]+", price_str)
    if match:
        price = match.group(0).replace(",", ".")
        try:
            return float(price)
        except ValueError:
            return None
    return None


def extract_image(image_element):
    srcset = image_element.attrib.get("srcset", None)
    if srcset:
        srcset_items = srcset.split(", ")
        srcset_images = []
        for item in srcset_items:
            parts = item.strip().split(" ")
            if len(parts) >= 2:
                try:
                    width = int(parts[1].replace("w", ""))
                    srcset_images.append((parts[0], width))
                except (ValueError, IndexError):
                    continue

        if srcset_images:
            largest_image = max(srcset_images, key=lambda x: x[1])
            return urljoin(BASE_URL, largest_image[0])
    return None
