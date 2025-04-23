import os
import base64
from PIL import Image
import io

# Create the directory if it doesn't exist
output_dir = "static/accessories/sunglasses"
os.makedirs(output_dir, exist_ok=True)

# Function to save base64 image
def save_base64_image(base64_string, output_path):
    try:
        # Remove the data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64 string
        image_data = base64.b64decode(base64_string)
        
        # Create PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Save image
        image.save(output_path, 'PNG')
        print(f"Successfully saved {output_path}")
    except Exception as e:
        print(f"Error saving {output_path}: {str(e)}")

# Base64 strings of your images (you'll need to replace these with the actual base64 strings)
images = {
    "sunglasses1.png": "YOUR_BASE64_STRING_1",
    "sunglasses2.png": "YOUR_BASE64_STRING_2",
    "sunglasses3.png": "YOUR_BASE64_STRING_3",
    "sunglasses4.png": "YOUR_BASE64_STRING_4",
    "sunglasses5.png": "YOUR_BASE64_STRING_5"
}

# Save each image
for filename, base64_string in images.items():
    output_path = os.path.join(output_dir, filename)
    save_base64_image(base64_string, output_path) 