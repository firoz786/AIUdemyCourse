"""
Day05_01_FileTools_DocumentProcessing: extends the Day04 "tools" idea with a
new file-reading tool, `read_text_file`, that lets an agent load the
contents of a document from disk so it can later be summarized, searched, or
reasoned about by an LLM. The time/dice/password tools are kept here too as
earlier examples of simple tools.
"""

from datetime import datetime


def get_current_time():
    """Return the current date and time."""

    # Format today's date/time as a human-readable string.
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")


import random


def roll_dice():
    """Return a random number between 1 and 6."""

    # Simulate rolling a standard six-sided die.
    return random.randint(1, 6)


import secrets
import string


def generate_password(length=12):
    """Generate a secure random password."""

    # Build the pool of characters a password can be made from: letters,
    # digits, and punctuation symbols.
    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ""

    # Pick one random character at a time using `secrets` (a
    # cryptographically secure random generator).
    for _ in range(length):
        password += secrets.choice(characters)

    return password


def read_text_file(filename):
    """Read and return the full contents of a text file as a string."""

    try:
        # Open and read the whole file in one go.
        with open(filename, "r") as file:
            return file.read()

    except FileNotFoundError:
        # Fail gracefully with a friendly message instead of crashing if the
        # file doesn't exist (e.g. wrong path typed by the user).
        return "Error: File not found."

