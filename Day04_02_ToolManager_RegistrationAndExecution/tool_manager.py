"""
Day04_02_ToolManager_RegistrationAndExecution: implements the `ToolManager`
class, which is the reusable "registry" of tools. It maps one or more text
aliases (e.g. "dice", "roll dice") to a `ToolCommand` describing a label and
a handler function to call. `execute()` looks up whatever the user typed and
either runs the matching tool or returns None so the caller knows to fall
back to a normal LLM chat call. This is the core idea behind tool
registration and dispatch in agent frameworks.
"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from tools import get_current_time, get_dice_roll, get_secret_password


@dataclass(frozen=True)
class ToolCommand:
    """Describe a command that can be invoked from the assistant prompt."""

    aliases: tuple[str, ...]
    label: str
    handler: Callable[[], object]


# The built-in tools this assistant knows about out of the box: each one has
# one or more text aliases a user can type to trigger it directly.
DEFAULT_TOOL_COMMANDS = (
    ToolCommand(("time", "clock"), "Current time", get_current_time),
    ToolCommand(("roll dice", "dice"), "Dice roll", get_dice_roll),
    ToolCommand(("secret password", "password"), "Secret password", get_secret_password),
)


class ToolManager:
    """Register tool aliases and execute matching user commands."""

    def __init__(self, commands: Iterable[ToolCommand] | None = None) -> None:
        # Maps a normalized alias string -> the ToolCommand that handles it.
        self._commands: dict[str, ToolCommand] = {}
        # Register either the caller-supplied commands or the defaults above.
        for command in DEFAULT_TOOL_COMMANDS if commands is None else commands:
            self.register(command)

    def register(self, command: ToolCommand) -> None:
        # Normalize aliases (trim whitespace, ignore case) so lookups are
        # forgiving of how the user types them.
        aliases = tuple(alias.strip().casefold() for alias in command.aliases)
        if not aliases or any(not alias for alias in aliases):
            raise ValueError("A tool command must have at least one non-empty alias.")
        if len(set(aliases)) != len(aliases):
            raise ValueError("Tool command aliases must be unique.")
        if any(alias in self._commands for alias in aliases):
            raise ValueError("Tool command aliases cannot overlap existing commands.")

        # Index every alias so execute() can find this command quickly.
        for alias in aliases:
            self._commands[alias] = command

    def execute(self, user_input: str) -> str | None:
        """Execute an exact alias match, or return None for regular chat input."""
        # Look up the normalized input; if nothing matches, this is not a
        # tool command - let the caller treat it as a normal chat message.
        command = self._commands.get(user_input.strip().casefold())
        if command is None:
            return None

        # Run the matched tool's handler function and format the result.
        return f"{command.label}: {command.handler()}"
