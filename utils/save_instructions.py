import os

def create_sunglasses_directory():
    """Create the sunglasses directory and print instructions"""
    # Create the directory
    output_dir = "static/accessories/sunglasses"
    os.makedirs(output_dir, exist_ok=True)
    
    # Print instructions
    print("\nInstructions for saving sunglasses images:")
    print("------------------------------------------")
    print("Please save the following images in this directory:")
    print(f"{os.path.abspath(output_dir)}\n")
    
    # List all images to save
    sunglasses = [
        ("sunglasses1.png", "Blue mirrored sunglasses"),
        ("sunglasses2.png", "White frame glasses"),
        ("sunglasses3.png", "Rose gold frame glasses"),
        ("sunglasses4.png", "White cat-eye glasses"),
        ("sunglasses5.png", "Black frame glasses")
    ]
    
    for filename, description in sunglasses:
        print(f"Save '{description}' as: {filename}")
        print(f"Full path: {os.path.join(os.path.abspath(output_dir), filename)}\n")
    
    print("\nImportant:")
    print("1. Save images in PNG format")
    print("2. Remove the black background")
    print("3. Make sure the images are properly cropped")
    print("4. Keep a reasonable size (around 400px width)")

if __name__ == "__main__":
    create_sunglasses_directory() 