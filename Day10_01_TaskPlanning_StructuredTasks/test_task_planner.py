"""
Day10_01_TaskPlanning_StructuredTasks - test_task_planner.py

A simple manual smoke-test script for task_planner.decompose_task(): it
feeds in a multi-part user request and prints the resulting task list so a
learner can see how the LLM splits one goal into several ordered,
executable sub-tasks.
"""

from task_planner import decompose_task

# A request with three distinct sub-goals, to show that decompose_task
# can split it into separate ordered tasks.
user_request = (
    "Get the current time, generate a secure password, and explain Python."
)

# Ask the LLM to break the request down into a task list.
tasks = decompose_task(user_request)

print("\nTask Plan")
print("---------")

for task in tasks:
    print("-", task)

