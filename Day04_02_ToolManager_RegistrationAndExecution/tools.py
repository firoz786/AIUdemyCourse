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

    character_groups = (
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    )
    alphabet = "".join(character_groups)
    password_characters = [secrets.choice(group) for group in character_groups]
    password_characters.extend(
        secrets.choice(alphabet) for _ in range(length - len(password_characters))
    )
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)
