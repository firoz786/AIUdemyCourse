"""
Day 14.05 - Parallel Agents with Concurrency: Parallel Demo
-------------------------------------------------------------------
This standalone script is the main new concept for Day 14.05. It defines
three "fake" agents (research, technology, market) that each just sleep
for a few seconds to simulate doing slow work (like calling an LLM or an
API). It then runs them two ways: SEQUENTIALLY (one after another, using
plain `await`) and in PARALLEL (all at once, using `asyncio.gather`). The
printed timings show that running independent agents concurrently can be
much faster than running them one by one, which matters once a
multi-agent system has several workers whose tasks don't depend on each
other.
"""

# Core library for writing asynchronous ("async") Python code: coroutines,
# event loop, and concurrency helpers like asyncio.gather().
import asyncio
# Standard library module used to measure how long each run takes.
import time


async def research_agent():
    # `async def` makes this a coroutine: a function that can pause (at
    # `await`) and let other coroutines run while it's "waiting".
    print("Research Agent started")

    # Simulate slow work (e.g. an LLM call) without blocking other coroutines.
    await asyncio.sleep(3)

    print("Research Agent finished")

    return "Research result"


async def technology_agent():
    print("Technology Agent started")

    # This agent simulates a shorter, 2-second task.
    await asyncio.sleep(2)

    print("Technology Agent finished")

    return "Technology result"


async def market_agent():
    print("Market Agent started")

    # This agent simulates the longest, 4-second task.
    await asyncio.sleep(4)

    print("Market Agent finished")

    return "Market result"


async def run_sequential():
    # Start a high-resolution timer so we can report how long this takes.
    start = time.perf_counter()

    # Each `await` here blocks until that agent finishes before starting the
    # next one, so total time = 3 + 2 + 4 = 9 seconds.
    research = await research_agent()

    technology = await technology_agent()

    market = await market_agent()

    elapsed = (
        time.perf_counter()
        - start
    )

    print("\nSequential Results:")

    print(research)
    print(technology)
    print(market)

    print(
        f"\nSequential time: "
        f"{elapsed:.2f} seconds"
    )


async def run_parallel():
    # Start a high-resolution timer so we can report how long this takes.
    start = time.perf_counter()

    # asyncio.gather() runs all three coroutines CONCURRENTLY and waits for
    # all of them to finish. Total time ≈ the slowest agent (4 seconds),
    # not the sum of all three, because they overlap while waiting.
    results = await asyncio.gather(
        research_agent(),
        technology_agent(),
        market_agent()
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    print("\nParallel Results:")

    for result in results:

        print(result)

    print(
        f"\nParallel time: "
        f"{elapsed:.2f} seconds"
    )


async def main():
    # Run the slow, one-at-a-time version first...
    print("=" * 50)
    print("SEQUENTIAL EXECUTION")
    print("=" * 50)

    await run_sequential()

    # ...then run the same three agents concurrently to compare timings.
    print("\n" + "=" * 50)
    print("PARALLEL EXECUTION")
    print("=" * 50)

    await run_parallel()


if __name__ == "__main__":
    # asyncio.run() creates an event loop, runs `main()` to completion, and
    # cleans up afterward - the recommended entry point for async scripts.
    asyncio.run(main())
