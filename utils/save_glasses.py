import os

def save_sunglasses():
    """Save sunglasses images with proper names"""
    # Create the sunglasses directory if it doesn't exist
    output_dir = "static/accessories/sunglasses"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the images with proper names
    sunglasses_names = [
        "sunglasses1.png",  # Blue mirrored sunglasses
        "sunglasses2.png",  # White frame glasses
        "sunglasses3.png",  # Rose gold frame glasses
        "sunglasses4.png",  # White cat-eye glasses
        "sunglasses5.png"   # Black frame glasses
    ]
    
    print("Saving sunglasses images...")
    for name in sunglasses_names:
        output_path = os.path.join(output_dir, name)
        print(f"Please save {name} in: {output_path}")

if __name__ == "__main__":
    save_sunglasses() 