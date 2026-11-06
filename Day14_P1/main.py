from manager import run_manager


def main():

    print("=" * 50)
    print(" MULTI-AGENT AI SYSTEM")
    print("=" * 50)

    task = input(
        "\nEnter your task: "
    )

    result = run_manager(
        task
    )

    print("\n" + "=" * 50)
    print(" RESEARCH")
    print("=" * 50)

    print(
        result["research"]
    )

    print("\n" + "=" * 50)
    print(" CODE")
    print("=" * 50)

    print(
        result["code"]
    )

    print("\n" + "=" * 50)
    print(" REVIEW")
    print("=" * 50)

    print(
        result["review"]
    )


if __name__ == "__main__":
    main()
