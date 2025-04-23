import cv2
import numpy as np
import os

def process_glasses_image(input_path, target_width=400):
    """
    Process glasses image to:
    1. Remove black background
    2. Add transparency
    3. Resize while maintaining aspect ratio
    """
    # Read the image
    image = cv2.imread(input_path)
    if image is None:
        return None
    
    # Convert BGR to BGRA
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    # Create alpha channel based on black background
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    
    # Refine mask to remove noise
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Apply mask to alpha channel
    image[:, :, 3] = mask
    
    # Crop the image to remove excess transparent areas
    coords = cv2.findNonZero(mask)
    x, y, w, h = cv2.boundingRect(coords)
    image = image[y:y+h, x:x+w]
    
    # Resize image while maintaining aspect ratio
    aspect_ratio = image.shape[1] / image.shape[0]
    target_height = int(target_width / aspect_ratio)
    resized_image = cv2.resize(image, (target_width, target_height))
    
    return resized_image

def save_processed_glasses(input_path, output_path):
    """Save processed glasses image to the specified path"""
    processed_image = process_glasses_image(input_path)
    if processed_image is None:
        return False
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    return cv2.imwrite(output_path, processed_image)

def save_sunglasses_with_transparency(image_data, output_path, target_width=400):
    """
    Save a sunglasses image with:
    1. Transparent background
    2. Proper sizing
    3. PNG format
    """
    # Convert image data to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        return False
    
    # Convert to RGBA
    rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    # Create mask for black background
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    
    # Clean up the mask
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Apply mask to alpha channel
    rgba[:, :, 3] = mask
    
    # Crop to remove excess transparent areas
    coords = cv2.findNonZero(mask)
    x, y, w, h = cv2.boundingRect(coords)
    cropped = rgba[y:y+h, x:x+w]
    
    # Resize while maintaining aspect ratio
    aspect_ratio = cropped.shape[1] / cropped.shape[0]
    target_height = int(target_width / aspect_ratio)
    resized = cv2.resize(cropped, (target_width, target_height))
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save as PNG with transparency
    return cv2.imwrite(output_path, resized)

def setup_accessories_folder():
    """Create necessary directories if they don't exist"""
    os.makedirs('static/accessories/sunglasses', exist_ok=True)
    os.makedirs('static/accessories/earrings', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    
def process_all_glasses():
    """Process all glasses in the source directory"""
    source_dir = "glasses_source"
    output_dir = "static/accessories/sunglasses"
    
    # Create directories if they don't exist
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each image in the source directory
    for i in range(1, 6):
        input_path = os.path.join(source_dir, f"sunglasses{i}.jpg")
        output_path = os.path.join(output_dir, f"sunglasses{i}.png")
        
        if os.path.exists(input_path):
            if save_processed_glasses(input_path, output_path):
                print(f"Successfully processed and saved {output_path}")
            else:
                print(f"Failed to process {input_path}")
        else:
            print(f"Warning: {input_path} not found") 