import asyncio

from agent import create_agent_instance
from .test_cases import test_cases
from .evaluate import check_tool


async def main():

    agent = await create_agent_instance()

    for test_case in test_cases:

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

