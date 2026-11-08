"""
Day 20.06 - Production Complete Agent API (evaluation).

A small fixed set of test questions paired with the tool each question is
expected to trigger. Used by run_evaluation.py to automatically sanity
check the agent's tool-selection behavior.
"""

test_cases = [
    {
        "question": "What is the current time?",
        "expected_tool": "current_time",
    },
    {
        "question": "Roll a dice.",
        "expected_tool": "roll_dice",
    },
    {
        "question": "Generate a 16-character password.",
        "expected_tool": "generate_password",
    },
]
