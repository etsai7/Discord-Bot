from PIL import Image, ImageDraw, ImageFont
import os


def add_letters_to_cube(base_image_path, left_letter, right_letter, base_image = None):
    """
    Add letters to the left and right faces of an isometric cube.

    Args:
        base_image_path (str): Path to the base cube image
        left_letter (str): Letter to place on the left face
        right_letter (str): Letter to place on the right face

    Returns:
        PIL.Image: The final image with letters added
    """

    # Load the base cube image
    try:
        if base_image is None:
            base_img = Image.open(base_image_path)
        else:
            base_img = base_image
    except FileNotFoundError:
        print(f"Error: Could not find {base_image_path}")
        return None

    # Convert to RGBA if not already
    if base_img.mode != 'RGBA':
        base_img = base_img.convert('RGBA')

    # Get image dimensions
    width, height = base_img.size

    # Create a copy to work on
    result_img = base_img.copy()
    draw = ImageDraw.Draw(result_img)

    # Try to load a font - adjust size based on image dimensions
    font_size = int(width * 0.40)  # Adjust this multiplier as needed

    try:
        # Try different font names that might be available
        font_names = ['Arial-Bold.ttf', 'arial.ttf', 'Arial.ttf', 'arial.TTF', 'ARIAL.TTF']
        font = None
        for font_name in font_names:
            try:
                font = ImageFont.truetype(font_name, font_size)
                # print(f"Font: {font_name}")
                break
            except:
                continue

        if font is None:
            # Fall back to default font
            font = ImageFont.load_default()
            print("Using default font (letters may appear smaller)")
    except:
        font = ImageFont.load_default()
        print("Using default font (letters may appear smaller)")

    # Define positions for left and right faces based on the cube geometry
    # Adjusted positions to center letters on their respective cube faces

    # Left face center position - moved up and adjusted horizontally
    left_face_x = int(width * 0.30)  # 30% from left edge (more centered on left face)
    left_face_y = int(height * 0.50)  # 55% from top (moved up)

    # Right face center position - moved up and adjusted horizontally
    right_face_x = int(width * 0.70)  # 70% from left edge (more centered on right face)
    right_face_y = int(height * 0.50)  # 55% from top (moved up)

    # Function to create transformed text for isometric faces
    def create_transformed_text(text, face_type):
        """
        Create a transformed text image for isometric cube faces
        face_type: 'left' or 'right'
        """
        # Create a temporary image for the text with larger dimensions
        temp_size = font_size * 2
        temp_img = Image.new('RGBA', (temp_size, temp_size), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)

        # Draw text on temporary image
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Center the text on temp image
        text_x = (temp_size - text_width) // 2
        text_y = (temp_size - text_height) // 2
        temp_draw.text((text_x, text_y), text, fill='white', font=font, stroke_width=2)

        # Apply transformations based on face type
        if face_type == 'left':
            # Transform for left face - skew to match left isometric face
            # Scale and skew to match the perspective
            transformed = temp_img.transform(
                (int(temp_size * 0.8), int(temp_size * 1.2)),
                Image.Transform.AFFINE,
                (1.0, 0.0, 100, -0.5, 1.0, 230),  # Skew matrix for left face
                resample=Image.Resampling.BICUBIC
            )
        else:  # right face
            # Transform for right face - skew to match right isometric face
            transformed = temp_img.transform(
                (int(temp_size * 0.8), int(temp_size * 1.2)),
                Image.Transform.AFFINE,
                (1.0, 0, 200, 0.5, 1.0, 90),  # Skew matrix for right face
                resample=Image.Resampling.BICUBIC
            )

        return transformed

    # Create transformed text images
    if left_letter:
        left_text_img = create_transformed_text(left_letter, 'left')
        # Paste at left face position
        paste_x = int(width * 0.05)  # Further left
        paste_y = int(height * 0.35)  # Adjusted position
        result_img.paste(left_text_img, (paste_x, paste_y), left_text_img)

    if right_letter:
        right_text_img = create_transformed_text(right_letter, 'right')
        # Paste at right face position
        paste_x = int(width * 0.55)  # Further right
        paste_y = int(height * 0.35)  # Adjusted position
        result_img.paste(right_text_img, (paste_x, paste_y), right_text_img)

    return result_img


def main():
    """
    Main function to create the cube with P and M letters like the example.
    """

    base_image_path = "./exts/image/resources/images/Base.png"

    # Check if base image exists
    if not os.path.exists(base_image_path):
        print(f"Error: {base_image_path} not found in current directory")
        print("Please make sure base.png is in the same directory as this script")
        return None

    # Create the cube with P and M letters
    result_image = add_letters_to_cube(base_image_path, "P", "M")

    if result_image:
        # Display the result
        result_image.show()
        return result_image
    else:
        print("Failed to create the image")
        return None


# Function to allow custom letters
def create_custom_cube(left_letter, right_letter, base_image):
    """
    Create a cube with custom letters.

    Args:
        left_letter (str): Letter for left face
        right_letter (str): Letter for right face
    """



    result_image = add_letters_to_cube("", left_letter, right_letter, base_image)

    if result_image:
        result_image.show()
        return result_image
    else:
        print("Failed to create the image")
        return None


if __name__ == "__main__":
    # Run the main function to create P-M cube like the example
    main()

    # Example of creating custom cubes:
    # create_custom_cube("A", "B")
    # create_custom_cube("X", "Y")