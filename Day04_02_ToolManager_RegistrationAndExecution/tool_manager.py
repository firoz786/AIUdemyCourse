from collections.abc import Callable, Iterable
from dataclasses import dataclass

from tools import get_current_time, get_dice_roll, get_secret_password


@dataclass(frozen=True)
class ToolCommand:
	"""Describe a command that can be invoked from the assistant prompt."""

	aliases: tuple[str, ...]
	label: str
	handler: Callable[[], object]


DEFAULT_TOOL_COMMANDS = (
	ToolCommand(("time", "clock"), "Current time", get_current_time),
	ToolCommand(("roll dice", "dice"), "Dice roll", get_dice_roll),
	ToolCommand(("secret password", "password"), "Secret password", get_secret_password),
)


class ToolManager:
	"""Register tool aliases and execute matching user commands."""

	def __init__(self, commands: Iterable[ToolCommand] | None = None) -> None:
		self._commands: dict[str, ToolCommand] = {}
		for command in DEFAULT_TOOL_COMMANDS if commands is None else commands:
			self.register(command)

	def register(self, command: ToolCommand) -> None:
		aliases = tuple(alias.strip().casefold() for alias in command.aliases)
		if not aliases or any(not alias for alias in aliases):
			raise ValueError("A tool command must have at least one non-empty alias.")
		if len(set(aliases)) != len(aliases):
			raise ValueError("Tool command aliases must be unique.")
		if any(alias in self._commands for alias in aliases):
			raise ValueError("Tool command aliases cannot overlap existing commands.")

		for alias in aliases:
			self._commands[alias] = command

	def execute(self, user_input: str) -> str | None:
		"""Execute an exact alias match, or return None for regular chat input."""
		command = self._commands.get(user_input.strip().casefold())
		if command is None:
			return None

		return f"{command.label}: {command.handler()}"
