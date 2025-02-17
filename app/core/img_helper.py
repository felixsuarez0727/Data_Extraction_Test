import os
import requests
from PIL import Image
from io import BytesIO
import cairosvg

SIZES = [(100, 100), (500, 500), (2000, 2000)]
def download_and_resize(image_url, category, product_id):
    images_folder = os.path.join("output", "images")
    os.makedirs(images_folder, exist_ok=True)

    base_filename = f"{category}_{product_id}"

    try:
        response = requests.get(image_url)
        response.raise_for_status()  

        if image_url.lower().endswith(".svg"):
            svg_file = BytesIO(response.content)

           
            output_png_path = os.path.join(images_folder, f"{base_filename}.png")
            cairosvg.svg2png(file_obj=svg_file, write_to=output_png_path)
           
            for size in SIZES:
                svg_file.seek(0) 
                resized_png_path = os.path.join(images_folder, f"{base_filename}_{size[0]}x{size[1]}.png")
                cairosvg.svg2png(
                    file_obj=svg_file,
                    write_to=resized_png_path,
                    output_width=size[0],
                    output_height=size[1],
                )
            
            os.remove(output_png_path)

        else:          
            img = Image.open(BytesIO(response.content))

            for size in SIZES:
                img_resized = resize_image_aspect(img, size)
                file_path = os.path.join(
                    images_folder, f"{base_filename}_{size[0]}x{size[1]}.jpg"
                )
                img_resized.save(file_path, "JPEG")
                

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
    except Exception as e:
        print(f"Error procesing image: {e}")


def resize_image_aspect(img, size):
    width, height = img.size

    aspect_ratio = width / height

    if width > height:
        new_width = size[0]
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = size[1]
        new_width = int(new_height * aspect_ratio)

    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - size[0]) / 2
    upper = (new_height - size[1]) / 2
    right = (new_width + size[0]) / 2
    lower = (new_height + size[1]) / 2

    img_resized = img_resized.crop((left, upper, right, lower))

    return img_resized

