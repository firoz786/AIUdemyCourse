"""
Day04_02_ToolManager_RegistrationAndExecution: defines the local Python
functions ("tools") that the ToolManager can register and run on behalf of
the user - getting the current time, rolling a dice, and generating a secure
password with guaranteed character variety. These are plain functions with
no AI involved; the "intelligence" is in how ToolManager decides when to
call them.
"""

import random
import secrets
import string
from datetime import datetime


def get_current_time() -> str:
    """Return the current date and time in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_dice_roll() -> int:
    """Return a random result from a six-sided die."""
    return random.randint(1, 6)


def get_secret_password(length: int = 12) -> str:
    """Generate a secure password containing each major character category."""
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    # Guarantee the password has at least one character from each of these
    # groups (lowercase, uppercase, digit, punctuation) for extra strength.
    character_groups = (
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    )
    alphabet = "".join(character_groups)
    # Start with one guaranteed character from each group...
    password_characters = [secrets.choice(group) for group in character_groups]
    # ...then fill the rest of the length with random characters from the
    # combined alphabet.
    password_characters.extend(
        secrets.choice(alphabet) for _ in range(length - len(password_characters))
    )
    # Shuffle so the guaranteed characters aren't always in the same order.
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)
