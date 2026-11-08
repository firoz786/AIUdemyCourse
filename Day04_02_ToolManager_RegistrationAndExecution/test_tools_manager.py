"""
Day04_02_ToolManager_RegistrationAndExecution: automated unit tests for the
tool functions (tools.py) and the ToolManager registry (tool_manager.py).
They check that each tool returns a sensibly-shaped value, that alias
lookups are case-insensitive, and that registering invalid/duplicate
commands raises errors as expected.
"""

import string
import unittest
from datetime import datetime

from tools import get_current_time, get_dice_roll, get_secret_password
from tool_manager import ToolCommand, ToolManager


class ToolTests(unittest.TestCase):
    def test_get_current_time_returns_formatted_timestamp(self):
        # The returned string should parse back into a real datetime using
        # the expected format.
        current_time = get_current_time()

        parsed_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

        self.assertIsInstance(parsed_time, datetime)

    def test_get_dice_roll_returns_value_between_one_and_six(self):
        # A six-sided die can only land on 1 through 6.
        dice_roll = get_dice_roll()

        self.assertIn(dice_roll, range(1, 7))

    def test_get_secret_password_returns_allowed_characters(self):
        # Check the password is the right length, uses only allowed
        # characters, and includes at least one of each required category.
        password = get_secret_password()
        allowed_characters = string.ascii_letters + string.digits + string.punctuation

        self.assertEqual(len(password), 12)
        self.assertTrue(all(character in allowed_characters for character in password))
        self.assertTrue(any(character in string.ascii_lowercase for character in password))
        self.assertTrue(any(character in string.ascii_uppercase for character in password))
        self.assertTrue(any(character in string.digits for character in password))
        self.assertTrue(any(character in string.punctuation for character in password))

    def test_get_secret_password_rejects_length_under_four(self):
        # Lengths below 4 cannot fit one character from every required
        # category, so this must raise.
        with self.assertRaises(ValueError):
            get_secret_password(3)

    def test_tool_manager_matches_aliases_case_insensitively(self):
        # Extra whitespace and mixed case should still match the "dice" alias.
        manager = ToolManager()

        result = manager.execute("  DICE  ")

        self.assertRegex(result, r"^Dice roll: [1-6]$")

    def test_tool_manager_returns_none_for_regular_chat(self):
        # Anything that isn't a known alias should fall through to normal chat.
        manager = ToolManager()

        self.assertIsNone(manager.execute("Tell me a joke"))

    def test_tool_manager_accepts_additional_commands(self):
        # Custom commands supplied by the caller should also be registered.
        manager = ToolManager(
            commands=(ToolCommand(("greet",), "Greeting", lambda: "Hello"),)
        )

        self.assertEqual(manager.execute("greet"), "Greeting: Hello")

    def test_tool_manager_rejects_duplicate_aliases(self):
        # Registering an alias that's already taken should raise an error.
        manager = ToolManager()

        with self.assertRaises(ValueError):
            manager.register(ToolCommand(("clock",), "Duplicate", lambda: "unused"))


if __name__ == "__main__":
    unittest.main()