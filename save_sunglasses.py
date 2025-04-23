from utils.image_processor import save_sunglasses_with_transparency
import os

def save_sunglasses_images(images_data):
    """Save the sunglasses images with proper processing"""
    output_dir = "static/accessories/sunglasses"
    os.makedirs(output_dir, exist_ok=True)
    
    # Names and descriptions for the sunglasses
    sunglasses = [
        ("sunglasses1.png", "Blue mirrored sunglasses"),
        ("sunglasses2.png", "White frame glasses"),
        ("sunglasses3.png", "Rose gold frame glasses"),
        ("sunglasses4.png", "White cat-eye glasses"),
        ("sunglasses5.png", "Black frame glasses")
    ]
    
    # Process each image
    for (filename, description), image_data in zip(sunglasses, images_data):
        output_path = os.path.join(output_dir, filename)
        if save_sunglasses_with_transparency(image_data, output_path):
            print(f"Successfully saved {description} as {filename}")
        else:
            print(f"Failed to save {description}")

if __name__ == "__main__":
    print("Please provide the sunglasses images to process") 