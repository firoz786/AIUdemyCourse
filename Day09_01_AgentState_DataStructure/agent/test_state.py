"""
Day09_01_AgentState_DataStructure - agent/test_state.py

A simple manual walkthrough script that exercises the state helper
functions defined in state.py. It creates a fresh agent state, simulates
one action/observation cycle (generating a password), advances the step
counter, then marks the state as finished -- printing the state dict at
each stage so a learner can see exactly how the data structure evolves.
"""

from state import *

# Step 1: Create a brand-new state for a given user request.
state = create_state(
    "Generate a password and tell me the current time."
)

print("Initial State")
print(state)

# Step 2: Simulate the agent deciding to call the "generate_password" tool.
add_action(
    state,
    "generate_password"
)

# Step 3: Simulate recording what that tool returned.
record_observation(
    state,
    "generate_password",
    "Password : X#8Lm@4P"
)

# Step 4: Advance to the next reasoning step.
next_step(state)

print("\nState After One Iteration")
print(state)

# Step 5: Mark the state as finished with the final answer for the user.
finish(
    state,
    "Password : X#8Lm@4P\nCurrent Time : 10:35 AM"
)

print("\nFinal State")
print(state)


