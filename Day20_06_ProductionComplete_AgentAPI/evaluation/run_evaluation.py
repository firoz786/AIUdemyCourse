"""
Day 20.06 - Production Complete Agent API (evaluation).

Entry point that runs a small automated test suite against the agent: for
each predefined test case it asks the agent a question and checks whether
the agent picked the correct tool to answer it, printing a PASS/FAIL report
for each case. Run with `python -m evaluation.run_evaluation` from the
project root.
"""

import asyncio

from agent import create_agent_instance
from .test_cases import test_cases
from .evaluate import check_tool


async def main():
    # Build a fresh agent instance (includes MCP tools + RAG tool).
    agent = await create_agent_instance()

    for test_case in test_cases:
        # Ask the agent the test question exactly as a real user would.
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": test_case["question"]
                    }
                ]
            }
        )

        # Did the agent call the tool we expected it to use?
        passed = check_tool(
            result,
            test_case["expected_tool"]
        )

        print(
            test_case["question"]
        )

        print(
            "Expected tool:",
            test_case["expected_tool"]
        )

        print(
            "Tool selection:",
            "PASS" if passed else "FAIL"
        )

        print()


if __name__ == "__main__":
    asyncio.run(main())

