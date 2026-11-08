"""
Day 14.02 - Dynamic Routing with an LLM Router: Entry Point
-------------------------------------------------------------
This script is the command-line entry point for the Day 14.02 demo. It
asks the user for a task, runs the agent pipeline via the Manager (which
now uses an LLM to decide, step by step, which worker runs next), and
prints the final research, code, and review once the Manager says the
run is finished.
"""

# Import the function that runs the whole multi-agent pipeline.
from manager import run_manager
# Standard library module needed for a clean exit on Ctrl+C / EOF.
import sys


def main():
    # Simple banner so the console output is easy to read.
    print("=" * 50)
    print(" INTELLIGENT MULTI-AGENT SYSTEM")
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

    # Run the manager, which repeatedly asks the LLM router which worker
    # should run next until it decides the pipeline is "finished".
    state = run_manager(
        task
    )

    # Display the research notes the Research Agent produced.
    print("\n" + "=" * 50)
    print(" RESEARCH")
    print("=" * 50)
    print(state["research"])

    # Display the code the Coding Agent produced.
    print("\n" + "=" * 50)
    print(" CODE")
    print("=" * 50)
    print(state["code"])

    # Display the Reviewer Agent's critique of that code.
    print("\n" + "=" * 50)
    print(" REVIEW")
    print("=" * 50)
    print(state["review"])


if __name__ == "__main__":
    main()
