import math
import os

from interactions import Extension, slash_command, SlashContext, slash_option, OptionType
from PIL import Image, ImageChops, ImageFont, ImageDraw

from src.exts.images.pezut import  pezut_helper


class Pezut(Extension):

    def make_text_image(self, letter: str, font: ImageFont.FreeTypeFont, angle: int) -> Image.Image:
        """
        Creates a rotated text image with transparent background
        """
        # Create a large transparent canvas
        img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Get text size
        bbox = font.getbbox(letter)  # returns (x0, y0, x1, y1)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        # Draw the letter centered
        draw.text(((200 - w) / 2 - bbox[0], (200 - h) / 2 - bbox[1]), letter, font=font, fill="white")

        # Rotate the text
        return img.rotate(angle, expand=True)

    def create_side_letter(self, letter: str, font: ImageFont.FreeTypeFont, side='left') -> Image.Image:
        """
        Creates a letter image transformed to fit a cube side (left or right) in isometric view.
        """
        canvas_size = 600
        img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        bbox = font.getbbox(letter)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        # Draw centered letter
        draw.text(
            ((canvas_size - w) / 2 - bbox[0], (canvas_size - h) / 2 - bbox[1]),
            letter, font=font, fill="white"
        )

        # Shear & rotate to match cube side
        if side == 'left':
            coeffs = (1, -0.5, 0, 0, 1, 0)  # lean left
            img = img.transform((canvas_size, canvas_size), Image.Transform.AFFINE, coeffs, resample=Image.Resampling.BICUBIC)
            img = img.rotate(-15, expand=True)
        elif side == 'right':
            coeffs = (1, 0.5, 0, 0, 1, 0)  # lean right
            img = img.transform((canvas_size, canvas_size), Image.Transform.AFFINE, coeffs, resample=Image.Resampling.BICUBIC)
            img = img.rotate(15, expand=True)
        return img

    def make_stretched_letter(self, letter: str, font: ImageFont.FreeTypeFont, stretch_factor: float) -> Image.Image:
        """
        Create a letter image and stretch it horizontally toward the center.
        """
        # Draw letter on large canvas
        canvas_size = 350
        img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        bbox = font.getbbox(letter)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        # Draw letter centered
        draw.text(
            ((canvas_size - w) / 2 - bbox[0], (canvas_size - h) / 2 - bbox[1]),
            letter, font=font, fill="white"
        )

        # Stretch horizontally
        new_w = int(canvas_size * stretch_factor)
        img = img.resize((new_w, canvas_size), resample=Image.Resampling.BICUBIC)

        return img

    def make_angled_letter(self, letter: str, font: ImageFont.FreeTypeFont, side='left', angle_deg=60) -> Image.Image:
        """
        Create a letter that is vertical at the edge and slopes toward center at angle_deg.
        """
        canvas_size = 600
        img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        bbox = font.getbbox(letter)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        # Draw letter centered
        draw.text(
            ((canvas_size - w) / 2 - bbox[0], (canvas_size - h) / 2 - bbox[1]),
            letter, font=font, fill="white"
        )

        # Compute shear offset
        angle_rad = math.radians(angle_deg)
        max_shear = canvas_size / 2  # limit shear so it stays inside canvas
        shear_offset = min(int(math.tan(angle_rad) * (canvas_size / 2)), max_shear)

        # Define QUAD coordinates inside canvas
        if side == 'left':
            # left vertical, right slanted down
            quad = [
                0, 0,  # top-left
                canvas_size, shear_offset,  # top-right
                canvas_size, canvas_size,  # bottom-right
                0, canvas_size  # bottom-left
            ]
        else:  # right
            # right vertical, left slanted down
            quad = [
                shear_offset, 0,  # top-left
                canvas_size, 0,  # top-right
                canvas_size, canvas_size,  # bottom-right
                shear_offset, canvas_size  # bottom-left
            ]

        # Transform letter with QUAD (output stays canvas_size x canvas_size)
        img = img.transform((canvas_size, canvas_size), Image.QUAD, quad, resample=Image.Resampling.BICUBIC)
        return img

    def helper_function(self, letter1, letter2, base_image):
        img = pezut_helper.create_custom_cube(letter1, letter2, base_image)
        return img

    @slash_command(name="pezut",
                   description="Pezut Image Generator")
    @slash_option(name="letter1",
                  description="The first letter of the image",
                  opt_type=OptionType.STRING,)
    @slash_option(name="letter2",
                  description="The second letter of the image",
                  opt_type=OptionType.STRING,)
    @slash_option(name="r",
                  description="Red in RGB",
                  opt_type=OptionType.INTEGER,
                  min_value=0,
                  max_value=255)
    @slash_option(name="g",
                  description="Green in RGB",
                  opt_type=OptionType.INTEGER,
                  min_value=0,
                  max_value=255)
    @slash_option(name="b",
                  description="Blue in RGB",
                  opt_type=OptionType.INTEGER,
                  min_value=0,
                  max_value=255)
    async def pezut_generator(self, ctx: SlashContext, letter1: str, letter2: str, r: int, g: int, b: int) -> None:
        base_image = Image.open('./exts/images/pezut/resources/images/Base.png').convert("RGBA")
        if r is None or g is None or b is None:
            color = (255, 0, 0, 100)
        else:
            color = (r, g, b, 100)
        zut_overlay = Image.new("RGBA", base_image.size, color)
        blended = Image.alpha_composite(base_image, zut_overlay)

        blek = Image.open('./exts/images/pezut/resources/images/Blek.png').convert("RGBA").resize(base_image.size)

        cube = ImageChops.subtract(blended, blek)

        output_path = './exts/images/pezut/outputs/images/pezut.png'
        cube = self.helper_function(letter1, letter2, cube)

        try:
            cube.save(output_path)
        except FileNotFoundError as e:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cube.save(output_path)

        await ctx.send(file=output_path, filename="pezut.png")



def setup(bot):
    Pezut(bot)