"""
Day 17.03 - Hierarchical Crew & Manager Delegation.

Entry point that runs two demos back to back: first the hierarchical crew
(manager delegates research/coding/review tasks), then a second crew that
demonstrates CrewAI memory by asking the researcher to recall a fact from
the earlier run.
"""

from crew import crew, memory_crew


def main():
    # Demo 1: hierarchical crew, manager-delegated tasks.
    result = crew.kickoff()

    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(result)
    print("\n")
    print("=" * 60)
    print("DEMO 2: CREWAI MEMORY")
    print("=" * 60)

    # Demo 2: a fresh crew run that relies on memory persisted from demo 1.
    memory_result = memory_crew.kickoff()

    print("\n")
    print("MEMORY RESULT")
    print("=" * 60)
    print(memory_result)


if __name__ == "__main__":
    main()
