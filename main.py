from Helper.word_search import create_word_search
from Helper.ITP import images_to_pdf
from dotenv import load_dotenv
import ast
import os

load_dotenv()

RED = '\033[31m'
GREEN = '\033[32m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Read words from file
def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        # Read all lines and parse them into a list of lists
        lines = file.readlines()
        words_list = [ast.literal_eval(line.strip()) for line in lines]
    return words_list

def delete_files_in_directory(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

                print(RED + '-' * 50 + RESET)
                print(RED + BOLD + f"Deleted file: {file_path}" + RESET)
                print(RED + '-' * 50 + RESET)
    else:
        print(RED + BOLD + f"****** Directory {directory} does not exist. ******" + RESET)

def delete_png_files_in_directory(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        count = 0
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and file_path.lower().endswith('.png'):
                os.remove(file_path)
                count+=1

        print(RED + '-' * 50 + RESET)
        print(RED + BOLD + f"Deleted PNG files: {count}" + RESET)
        print(RED + '-' * 50 + RESET)
    else:
        print(RED + BOLD + f"****** Directory {directory} does not exist. ******" + RESET)

# Read words from words.txt
words_to_find = read_words_from_file('words.txt')

image_directory = "output"
delete_files_in_directory(image_directory)

# Iterate over each word set and generate word search puzzles and solutions
for idx, words in enumerate(words_to_find, start=1):
    create_word_search(words, grid_size=15, output_dir=image_directory, output_file=f"{idx}.png")

output_pdf = "output/book.pdf"
image_folder = image_directory
page_width = float(os.getenv("PDF_PAGE_WIDTH")) * 2.83
page_height = float(os.getenv("PDF_PAGE_HEIGHT")) * 2.83
scale_factor = float(os.getenv("SCALE_FACTOR"))
font_path = os.getenv("FONT_PATH")
font_name = os.getenv("FONT_NAME")
images_to_pdf(image_folder, output_pdf, page_width, page_height, font_path, font_name, scale_factor)

delete_png_files_in_directory(image_directory)

# ANSI escape codes for styling the terminal output

print(GREEN + '-' * 50 + RESET)
print(GREEN + BOLD + f"PDF created successfully: {output_pdf}" + RESET)
print(GREEN + '-' * 50 + RESET)
