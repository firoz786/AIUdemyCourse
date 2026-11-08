"""
Day 17.01 - CrewAI Role-Based Agents.

Entry point for the sequential crew demo: it kicks off the crew (which
runs the researcher -> coder -> reviewer tasks in order) and prints the
final aggregated result to the console.
"""

from crew import crew


def main():
    # kickoff() runs every task in the crew's process order and returns
    # the final task's output.
    result = crew.kickoff()

    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()


