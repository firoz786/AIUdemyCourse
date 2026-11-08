"""
Day 17.02 - CrewAI with MCP Tool Integration.

Entry point: kicks off the crew (whose researcher agent calls an MCP tool
mid-task) and prints the final result.
"""

from crew import crew


def main():
    # kickoff() runs every task in order and returns the final task's output.
    result = crew.kickoff()

    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()

