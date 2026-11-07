from crew import crew , memory_crew


def main():

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

    memory_result = memory_crew.kickoff()

    print("\n")
    print("MEMORY RESULT")
    print("=" * 60)

    print(memory_result)


if __name__ == "__main__":
    main()
