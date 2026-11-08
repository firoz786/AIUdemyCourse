"""
Day 14.05 - Parallel Agents with Concurrency: Entry Point
-------------------------------------------------------------------
Command-line entry point for the Day 14.05 demo's sequential pipeline
(identical to Day 14.04: ask for a task, run the Manager, print
research/code/review). The new concurrency concept for this day is shown
separately in parallel_demo.py - run that file directly to see sequential
vs. parallel execution timing side by side.
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

    # Run the manager, which loops research -> coding -> review (capped at
    # MAX_REVISIONS rounds) until the reviewer approves or the cap is hit.
    state = run_manager(
        task
    )

    # Display the research notes the Research Agent produced.
    print("\n" + "=" * 50)
    print(" RESEARCH")
    print("=" * 50)
    print(state["research"])

    # Display the final code the Coding Agent produced.
    print("\n" + "=" * 50)
    print(" CODE")
    print("=" * 50)
    print(state["code"])

    # Display the Reviewer Agent's final structured verdict.
    print("\n" + "=" * 50)
    print(" REVIEW")
    print("=" * 50)
    print(state["review"])


if __name__ == "__main__":
    main()
