from utils.image_processor import save_processed_glasses
import os

def process_shared_images(images_data):
    """Process the shared sunglasses images"""
    output_dir = "static/accessories/sunglasses"
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, image_data in enumerate(images_data, 1):
        output_path = os.path.join(output_dir, f"sunglasses{idx}.png")
        if save_processed_glasses(image_data, output_path):
            print(f"Successfully saved sunglasses{idx}.png")
        else:
            print(f"Failed to process sunglasses{idx}")

if __name__ == "__main__":
    # Here you would pass the image data from the shared images
    print("Please provide the image data to process the sunglasses") 