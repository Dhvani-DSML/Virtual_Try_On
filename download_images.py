import os
import shutil
from PIL import Image
import numpy as np

def copy_and_save_image(src_path, output_path):
    try:
        # Copy the file
        shutil.copy2(src_path, output_path)
        print(f"Successfully copied {src_path} to {output_path}")
        
        # Verify the image can be opened
        try:
            with Image.open(output_path) as img:
                print(f"Verified image {output_path} - Size: {img.size}")
        except Exception as e:
            print(f"Warning: Copied file {output_path} but couldn't verify as image: {str(e)}")
            
    except Exception as e:
        print(f"Error copying {src_path}: {str(e)}")

# Image configurations
images = {
    "sunglasses": {
        "sunglasses1.png": r"C:\Users\Dhvani\Pictures\glasses dataset\2001.png",
        "sunglasses2.png": r"C:\Users\Dhvani\Pictures\glasses dataset\2002.png",
        "sunglasses3.png": r"C:\Users\Dhvani\Pictures\glasses dataset\2003.png",
        "sunglasses4.png": r"C:\Users\Dhvani\Pictures\glasses dataset\2004.png",
        "sunglasses5.png": r"C:\Users\Dhvani\Pictures\glasses dataset\2005.png"
    },
    "hats": {
        "hat1.png": r"C:\Users\Dhvani\Pictures\hat dataset\2001.png",
        "hat2.png": r"C:\Users\Dhvani\Pictures\hat dataset\2002.png",
        "hat3.png": r"C:\Users\Dhvani\Pictures\hat dataset\2004.png",
        "hat4.png": r"C:\Users\Dhvani\Pictures\hat dataset\2005.png"
    }
}

# Process each category
for category, category_images in images.items():
    # Create category directory
    output_dir = f"static/accessories/{category}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy images for this category
    for dest_name, src_path in category_images.items():
        output_path = os.path.join(output_dir, dest_name)
        copy_and_save_image(src_path, output_path)
    
    print(f"\nAll {category} images have been copied to:", os.path.abspath(output_dir)) 