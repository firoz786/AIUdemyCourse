"""
Day 15 - Production Engineering & Resilience: Entry Point / CLI.

This is the command-line entry point that ties all the resilience concepts
together: it collects a task from the user, validates and runs it through the
multi-agent manager (which itself uses retrying LLM calls, logging, and
permission checks), and prints the results. It also demonstrates graceful
handling of Ctrl+C so an interactive user can cancel without an ugly crash,
and shows how tool permissions are enforced for each worker agent.
"""

import sys

# The manager coordinates the research/coding/review worker agents.
from agent.manager import run_manager

# Demonstrates which tools each agent role is allowed to use.
from permissions import (
    demonstrate_permissions
)


def main():
    # Simple banner so the console output is easy to read.
    print("=" * 50)
    print(" INTELLIGENT MULTI-AGENT SYSTEM")
    print("=" * 50)

    try:
        # Ask the user what they want the agent system to do.
        task = input(
            "\nEnter your task: "
        )
    except (KeyboardInterrupt, EOFError):
        # Let the user cancel cleanly with Ctrl+C instead of a stack trace.
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)

    try:
        # Run the task through the manager, which validates it and
        # orchestrates the research/coding/review workers with retries.
        state = run_manager(
        task
        )

    except ValueError as e:
        # Raised by validate_task() when the task is empty/too long.
        print(
        f"\nValidation error: {e}"
        )

    return

    print("\n" + "=" * 50)
    print(" RESEARCH")
    print("=" * 50)
    print(state["research"])

    print("\n" + "=" * 50)
    print(" CODE")
    print("=" * 50)
    print(state["code"])

    print("\n" + "=" * 50)
    print(" REVIEW")
    print("=" * 50)
    print(state["review"])

    demonstrate_permissions()


if __name__ == "__main__":
    main()

    print("\n" + "=" * 50)
    print(" RESEARCH")
    print("=" * 50)
    print(state["research"])

    print("\n" + "=" * 50)
    print(" CODE")
    print("=" * 50)
    print(state["code"])

    print("\n" + "=" * 50)
    print(" REVIEW")
    print("=" * 50)
    print(state["review"])

    demonstrate_permissions()


if __name__ == "__main__":
    main()
