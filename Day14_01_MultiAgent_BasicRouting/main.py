"""
Day 14.01 - Multi-Agent Basic Routing: Entry Point
--------------------------------------------------------
This script is the command-line entry point for the Day 14.01 demo. It
asks the user for a task, runs the hardcoded Research -> Code -> Review
pipeline via the Manager, and then prints each agent's output to the
console. This demonstrates the simplest possible multi-agent setup before
we add dynamic routing in later days.
"""

# Import the function that runs the whole multi-agent pipeline.
from manager import run_manager
# Standard library module needed for a clean exit on Ctrl+C / EOF.
import sys


def main():
    # Simple banner so the console output is easy to read.
    print("=" * 50)
    print(" MULTI-AGENT AI SYSTEM")
    print("=" * 50)

    # Ask the user what they want the agents to build. Wrapped in try/except
    # so Ctrl+C (KeyboardInterrupt) or Ctrl+D/EOF exits gracefully instead of
    # printing a scary traceback.
    try:
        task = input(
            "\nEnter your task: "
        )
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)

    # Run the manager, which internally calls Research -> Coding -> Review.
    result = run_manager(
        task
    )

    # Display the research notes the Research Agent produced.
    print("\n" + "=" * 50)
    print(" RESEARCH")
    print("=" * 50)

    print(
        result["research"]
    )

    # Display the code the Coding Agent produced.
    print("\n" + "=" * 50)
    print(" CODE")
    print("=" * 50)

    print(
        result["code"]
    )

    # Display the Reviewer Agent's critique of that code.
    print("\n" + "=" * 50)
    print(" REVIEW")
    print("=" * 50)

    print(
        result["review"]
    )


if __name__ == "__main__":
    main()
