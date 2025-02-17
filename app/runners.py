from database.db import initialize_db
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapper.spider import MainSpider
from core.db_helper import get_all_products
from core.img_helper import download_and_resize
from core.csv_helper import write_products_to_csv
from tqdm import tqdm

import shutil
import os


def run_cleanup(output_dir="output"):
    try:
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            shutil.rmtree(output_dir)
            print(f"⚠️  '{output_dir}' and all its contents have been deleted.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ '{output_dir}' has been successfully created.")


def run_database():
    initialize_db()
    print("✅ 'database' has been successfully created.")


def run_scraper():
    print("✅ 'scraper' initialized successfully.")
    process = CrawlerProcess(get_project_settings())
    process.crawl(MainSpider)
    process.start()
    print("✅ 'scraper' ended successfully.")


def run_image_processing():
    products = get_all_products()
    for product in tqdm(products, desc="Procesando productos", unit="producto"):
        download_and_resize(
            product.get("image_url"), product.get("category"), product.get("id")
        )

    print("✅ 'images' have been processed.")


def run_csv_generation():
    products = get_all_products()
    write_products_to_csv(products)
    print("✅ 'csv' files have been created.")
