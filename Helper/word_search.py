from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import random
import os

load_dotenv()

def create_word_search(words, grid_size=15, output_dir="output", output_file="word_search.png"):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # right, down, diagonal-right, diagonal-left
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    word_positions = []  # To store the positions of words for the solution

    def can_place_word(word, row, col, delta_row, delta_col):
        for i in range(len(word)):
            new_row = row + i * delta_row
            new_col = col + i * delta_col
            if new_row < 0 or new_row >= grid_size or new_col < 0 or new_col >= grid_size:
                return False
            if grid[new_row][new_col] not in (' ', word[i]):
                return False
        return True

    def place_word(word):
        placed = False
        while not placed:
            direction = random.choice(directions)
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)
            if can_place_word(word, row, col, *direction):
                positions = []
                for i in range(len(word)):
                    new_row = row + i * direction[0]
                    new_col = col + i * direction[1]
                    grid[new_row][new_col] = word[i]
                    positions.append((new_row, new_col))
                word_positions.append((word, positions))
                placed = True

    for word in words:
        place_word(word.replace(" ", "").upper())

    # Fill empty cells with random letters
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Create images
    cell_size = 60
    img_width = grid_size * cell_size
    img_height = img_width + 200  # Increased space between grid and words + more space below words

    try:
        font = ImageFont.truetype(os.getenv("FONT_PATH"), 28)
        bold_font = ImageFont.truetype(os.getenv("FONT_BOLD_PATH"), 28)
    except:
        font = ImageFont.load_default()
        bold_font = font
        print("****************** load default font ******************")

    def draw_grid(draw, grid, highlight_positions=None):
        # Draw the grid without internal borders for cells containing letters
        for i in range(grid_size):
            for j in range(grid_size):
                x = j * cell_size
                y = i * cell_size

                # Highlight cells if needed
                if highlight_positions and (i, j) in highlight_positions:
                    draw.rectangle([x, y, x + cell_size, y + cell_size], fill='lightgray', outline='black', width=2)
                    letter_font = bold_font
                    letter_color = "green"
                else:
                    letter_font = font
                    letter_color = "black"

                # Draw letter
                letter = grid[i][j]
                bbox = draw.textbbox((0, 0), letter, font=letter_font)
                text_x = x + (cell_size - (bbox[2] - bbox[0])) // 2
                text_y = y + (cell_size - (bbox[3] - bbox[1])) // 2
                draw.text((text_x, text_y), letter, fill=letter_color, font=letter_font)

        # Draw outer border around the whole grid
        draw.rectangle([0, 0, img_width, img_width], outline='black', width=3)

    # Word search image
    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)
    draw_grid(draw, grid)

    # Space between grid and word list
    word_area_top = img_width + 20  # Space added between grid and word list
    draw.rectangle([0, word_area_top, img_width, img_height], fill='white')

    # Display words in three columns
    words_per_column = (len(words) + 2) // 3
    column_width = img_width // 3
    for col in range(3):
        col_x = column_width * col
        for i in range(words_per_column):
            word_idx = i + col * words_per_column
            if word_idx < len(words):
                word = words[word_idx]
                word_bbox = draw.textbbox((0, 0), word, font=font)
                text_x = col_x + (column_width - (word_bbox[2] - word_bbox[0])) // 2
                text_y = word_area_top + 10 + i * 40
                draw.text((text_x, text_y), word, fill='black', font=font)

    # Add space below the words list
    img_height_with_margin = img_height + 50  # Extra space below words

    word_search_file = f"Puzzle_{output_file}"
    word_search_path = os.path.join(output_dir, word_search_file)
    img.save(word_search_path)

    # Solution image
    solution_img = Image.new('RGB', (img_width, img_height_with_margin), color='white')
    solution_draw = ImageDraw.Draw(solution_img)
    highlight_positions = [pos for word, positions in word_positions for pos in positions]
    draw_grid(solution_draw, grid, highlight_positions=highlight_positions)
    solution_draw.rectangle([0, word_area_top, img_width, img_height_with_margin], fill='white')
    for col in range(3):
        col_x = column_width * col
        for i in range(words_per_column):
            word_idx = i + col * words_per_column
            if word_idx < len(words):
                word = words[word_idx]
                word_bbox = solution_draw.textbbox((0, 0), word, font=font)
                text_x = col_x + (column_width - (word_bbox[2] - word_bbox[0])) // 2
                text_y = word_area_top + 10 + i * 40
                solution_draw.text((text_x, text_y), word, fill='black', font=font)

    solution_file = f"Solution_{output_file}"
    solution_path = os.path.join(output_dir, solution_file)
    solution_img.save(solution_path)

    print(f"Word search saved to {word_search_path}")
    print(f"Solution saved to {solution_path}")
