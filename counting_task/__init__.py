from otree.api import *
import random
import os
import uuid
from PIL import Image, ImageDraw, ImageFont


doc = """
Counting Task App - Participants count ones in randomly generated binary table images
"""


class C(BaseConstants):
    NAME_IN_URL = "counting_task"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    counted_ones = models.IntegerField(
        label="How many ones do you count in the image?", min=0, max=100
    )
    correct_ones = models.IntegerField(blank=True, null=True)
    image_path = models.StringField(blank=True, null=True)


# PAGES
class Setup(WaitPage):
    def after_all_players_arrive(group):
        """
        Generate binary table and image before moving to the Task page.
        """
        for player in group.get_players():
            # Generate RANDOM_COLLECTION binary table
            table_data, actual_count = generate_binary_table(min_ones=37, max_ones=37)
    
            # Create image from table data
            image_path = create_binary_table_image(table_data)
    
            # Store the correct count and image path in Player model
            player.correct_ones = actual_count
            player.image_path = image_path


class Task(Page):
    form_model = "player"
    form_fields = ["counted_ones"]

    def error_message(player, values):
        """
        Validate form input for counted_ones field.
        """
        if values["counted_ones"] is not None:
            if values["counted_ones"] < 0:
                return "Please enter a non-negative number."
            if values["counted_ones"] > 100:  # Reasonable upper bound for 10x10 grid
                return "Please enter a reasonable count (maximum 100 for a 10x10 grid)."


# FUNCTIONS
def generate_binary_table(grid_size=10, min_ones=5, max_ones=25):
    """
    Generate a RANDOM_COLLECTION NxN binary table with configurable parameters.

    Args:
        grid_size (int): Size of the NxN grid (default: 10)
        min_ones (int): Minimum number of ones to place (default: 5)
        max_ones (int): Maximum number of ones to place (default: 25)

    Returns:
        tuple: (table_data, actual_count)
            - table_data: 2D list representing the binary table
            - actual_count: int representing the actual number of ones placed
    """
    # Initialize grid with all zeros
    table = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Determine RANDOM_COLLECTION number of ones to place
    num_ones = random.randint(min_ones, max_ones)

    # Ensure we don't try to place more ones than available cells
    max_possible_ones = grid_size * grid_size
    if num_ones > max_possible_ones:
        num_ones = max_possible_ones

    # Generate all possible positions
    all_positions = [(row, col) for row in range(grid_size) for col in range(grid_size)]

    # Randomly select positions for ones
    selected_positions = random.sample(all_positions, num_ones)

    # Place ones in selected positions
    for row, col in selected_positions:
        table[row][col] = 1

    return table, num_ones


def create_binary_table_image(table_data, cell_size=40):
    """
    Convert binary table data into PNG image with grid visualization using Pillow.

    Args:
        table_data (list): 2D list representing the binary table
        cell_size (int): Size of each cell in pixels (default: 40)

    Returns:
        str: Relative path to the generated PNG image file
    """
    grid_size = len(table_data)
    image_size = grid_size * cell_size + 1  # +1 for the border

    # Generate unique filename
    unique_id = str(uuid.uuid4())[:8]
    filename = f"binary_table_{unique_id}.png"

    # Create static directory if it doesn't exist
    static_dir = os.path.join(os.path.dirname(__file__), "static/counting_task")
    os.makedirs(static_dir, exist_ok=True)

    # Create image with white background
    image = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(image)

    # Try to load a font, fall back to default if not available
    try:
        font_size = int(cell_size * 0.6)
        font = ImageFont.truetype("Arial.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.load_default()
        except:
            font = None

    # Draw the grid and numbers
    for row in range(grid_size):
        for col in range(grid_size):
            # Calculate cell boundaries
            x = col * cell_size
            y = row * cell_size

            # Draw cell border
            draw.rectangle(
                [x, y, x + cell_size, y + cell_size],
                outline="black",
                fill="white",
                width=1,
            )

            # Draw the number (0 or 1) in the center of the cell
            number = str(table_data[row][col])

            if font:
                # Get text bounding box for centering
                bbox = draw.textbbox((0, 0), number, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                text_x = x + (cell_size - text_width) // 2
                text_y = y + (cell_size - text_height) // 2 - 3  # Slight adjustment for vertical centering

                draw.text((text_x, text_y), number, fill="black", font=font)
            else:
                # Fallback without font
                text_x = x + cell_size // 2 - 5
                text_y = y + cell_size // 2 - 8
                draw.text((text_x, text_y), number, fill="black")

    # Save the PNG file
    image_path = os.path.join(static_dir, filename)
    image.save(image_path, "PNG")

    # Return relative path for template use
    return f"counting_task/{filename}"


page_sequence = [Setup, Task]
