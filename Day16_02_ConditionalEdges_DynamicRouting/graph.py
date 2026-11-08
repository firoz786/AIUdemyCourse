"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph).

This file builds the actual LangGraph graph used in this lesson. Unlike the
simpler "BasicGraph" lesson (Day16_01) where nodes always flow to a fixed
next node, here we use `add_conditional_edges(...)` so the graph can look at
the CURRENT STATE after a node runs and dynamically decide which node to
visit next (e.g. "keep planning/acting" vs "stop and answer"). The graph
wires together three nodes - planner, tool, answer - and two routing
functions that branch based on state, forming a loop: plan -> act -> decide
whether to loop again or finish -> produce a final answer.
"""

from typing import TypedDict

# LangGraph building blocks: StateGraph holds nodes/edges, START/END are the
# special "entry" and "exit" markers of the graph.
from langgraph.graph import (
    StateGraph,
    START,
    END
)

# The three pieces of agent "thinking" reused from earlier lessons: decide
# the next action, run that action, and turn the final state into an answer.
from agent.planner import planner
from agent.executor import execute_action
from agent.runner import format_answer


# AgentState is the shared "memory" that flows through every node in the
# graph. Each node receives it, reads what it needs, and returns a partial
# dict of updates that LangGraph merges back into the state.
class AgentState(TypedDict):
    user_request: str      # The original question/task from the user.
    current_step: int      # How many planner/tool iterations have run so far.
    max_steps: int          # Safety limit to stop infinite planning loops.
    actions: list            # History of every action (tool name) chosen.
    observations: list      # History of results returned by each tool call.
    action: str              # The action the planner just chose this turn.
    finished: bool            # True once the agent is done and ready to answer.
    final_answer: str        # The natural-language answer shown to the user.


def create_planner_node(tools):
    """
    Factory function that returns a LangGraph node for the "planner" step.
    We use a factory (instead of a plain function) so the node closure can
    "remember" the list of available `tools` without needing to store them
    inside the graph state itself.
    """

    def planner_node(
        state: AgentState
    ):
        # Ask the LLM-based planner which tool to use next (or "FINISH").
        action = planner(
            state,
            tools
        )

        print("\nPlanner Selected:")
        print(action)

        # Return only the state fields this node changes; LangGraph merges
        # this into the full state automatically.
        return {
            "action": action,
            "finished": action == "FINISH"
        }

    return planner_node


def create_tool_node(client):
    """
    Factory function that returns a LangGraph node for the "tool" step.
    The MCP `client` is captured in the closure so the node can call tools
    on the running MCP server without passing the client through state.
    """

    async def tool_node(
        state: AgentState
    ):
        # Read the action the planner node chose in the previous step.
        action = state["action"]

        # Execute that action (tool call) via MCP and get its result text.
        observation = await execute_action(
            action,
            state,
            client
        )

        print("\nTool Observation:")
        print(observation)

        # Append this step's action/observation to the running history and
        # advance the step counter - this is what the routing logic below
        # uses to decide whether to keep looping.
        return {
            "observations": (
                state["observations"]
                + [
                    {
                        "step": state["current_step"],
                        "action": action,
                        "observation": observation
                    }
                ]
            ),
            "actions": (
                state["actions"]
                + [action]
            ),
            "current_step": (
                state["current_step"] + 1
            )
        }

    return tool_node


def answer_node(
    state: AgentState
):
    """
    Final node: turns the accumulated actions/observations into a friendly
    natural-language answer for the user.
    """

    answer = format_answer(
        state
    )

    print("\nFinal Answer:")
    print(answer)

    return {
        "final_answer": answer,
        "finished": True
    }


def route_after_planner(
    state: AgentState
):
    """
    CONDITIONAL EDGE function (core concept of this lesson): LangGraph calls
    this after the "planner" node runs, passing it the latest state. The
    string we return ("finish" or "tool") tells LangGraph which node to go
    to next - this is "dynamic routing" because the path is decided at
    runtime based on state, not hard-coded in advance.
    """

    if state["action"] == "FINISH":
        return "finish"

    return "tool"


def route_after_tool(
    state: AgentState
):
    """
    CONDITIONAL EDGE function called after the "tool" node runs. It checks
    the step counter against the max_steps safety limit to decide whether
    the agent should keep looping back to the planner ("continue") or stop
    and jump to the answer node ("stop").
    """

    if (
        state["current_step"]
        >= state["max_steps"]
    ):
        return "stop"

    return "continue"


def build_graph(
    tools,
    client
):
    """
    Assembles the StateGraph: register each node, wire the fixed edges,
    and wire the conditional edges that implement dynamic routing.
    """

    # Create a new graph whose shared state shape is AgentState.
    builder = StateGraph(
        AgentState
    )

    # Register each node under a name so edges can reference it by string.
    builder.add_node(
        "planner",
        create_planner_node(tools)
    )

    builder.add_node(
        "tool",
        create_tool_node(client)
    )

    builder.add_node(
        "answer",
        answer_node
    )

    # Fixed edge: the graph always starts by running the planner node.
    builder.add_edge(
        START,
        "planner"
    )

    # Conditional edge: after "planner" runs, call route_after_planner to
    # decide whether to go to "tool" or jump straight to "answer".
    builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "tool": "tool",
            "finish": "answer"
        }
    )

    # Conditional edge: after "tool" runs, call route_after_tool to decide
    # whether to loop back to "planner" or stop at "answer".
    builder.add_conditional_edges(
        "tool",
        route_after_tool,
        {
            "continue": "planner",
            "stop": "answer"
        }
    )

    # Fixed edge: once "answer" runs, the graph execution ends.
    builder.add_edge(
        "answer",
        END
    )

    # Compile the builder into a runnable graph object.
    return builder.compile()
