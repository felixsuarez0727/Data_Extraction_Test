import csv
import os

def write_products_to_csv(products):
    output_path = "output/data.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if not products:
        return

    with open(output_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
