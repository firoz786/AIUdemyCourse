"""
Day16_01 - LangGraph Basic Graph: manual state walkthrough (reference).

This script is a small, non-LangGraph demonstration of how the agent
state evolves over time: creating an initial state, recording an action
and its observation, advancing the step counter, and finally marking the
state as finished with an answer. It's meant to help you see state
mutations in isolation before tracing how the same state flows through
LangGraph nodes in graph.py.
"""

# NOTE: these helper functions (create_state, add_action, record_observation,
# next_step, finish) come from an earlier lesson's state module; this file
# demonstrates the *concept* of state transitions used by AgentState.
from Day09.agent.state import *

# Build the initial state for a new user request.
state = create_state(
    "Generate a password and tell me the current time."
)

print("Initial State")
print(state)

# Record that we performed the "generate_password" action.
add_action(
    state,
    "generate_password"
)

# Store the result/observation of that action.
record_observation(
    state,
    "generate_password",
    "Password : X#8Lm@4P"
)

# Advance the step counter after completing one plan/act/observe cycle.
next_step(state)

print("\nState After One Iteration")
print(state)

# Mark the state as finished, attaching the final combined answer.
finish(
    state,
    "Password : X#8Lm@4P\nCurrent Time : 10:35 AM"
)

print("\nFinal State")
print(state)
