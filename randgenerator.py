import random
import os

# Replace with all applicable terms for whatever experiment you're doing
term_list = ["Center", "Left", "Right", "Up", "Down"]

# How many terms should be generated
TOTAL_TERMS = 100

# Path to file (replace end with desired filename)
PATH_TO_FILE = "./configs/arrowfile1.txt"

with open(PATH_TO_FILE, mode="x") as file:
    for _ in range(TOTAL_TERMS):
        file.write(random.choice(term_list) + "\n")
