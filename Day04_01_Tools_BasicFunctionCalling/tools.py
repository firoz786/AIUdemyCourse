"""
Day04_01_Tools_BasicFunctionCalling: defines a handful of simple Python
functions ("tools") that an AI agent could call to do things an LLM cannot
do on its own - get the real current time, roll a dice, or generate a secure
random password. This file has no AI code in it; it just shows what a "tool"
looks like before we wire it up to an LLM's function-calling feature.
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
    # cryptographically secure random generator, safer than `random` for
    # anything security-related like passwords).
    for _ in range(length):
        password += secrets.choice(characters)

    return password
