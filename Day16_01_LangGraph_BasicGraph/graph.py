"""
Day16_01 - LangGraph Basic Graph.

This file shows the simplest possible LangGraph workflow: a graph made of
a single node wired together with a START and an END edge. LangGraph models
an agent as a graph where "nodes" are functions that read/update a shared
"state" dictionary, and "edges" describe which node runs next. Here we only
have one node ("planner") so the flow is linear: START -> planner -> END,
with no branching/conditional logic yet (that comes in later lessons).
"""

# StateGraph builds the graph, START/END are special markers for the
# entry point and exit point of the graph.
from langgraph.graph import (
    StateGraph,
    START,
    END
)

# planner() is the plain Python function that decides the next action;
# we will wrap it so LangGraph can call it as a graph node.
from agent.planner import planner

# AgentState is the TypedDict schema describing the shape of our shared state.
from agent.state import AgentState


def create_planner_node(tools):
    # Factory function: returns a node function that already "knows" about
    # the available tools, since LangGraph nodes only receive the state.

    def planner_node(state: AgentState):
        # Ask the planner (an LLM call) which action/tool to use next.
        action = planner(
            state,
            tools
        )

        # Teaching aid: show what the planner decided on each run.
        print("\nPlanner Selected:")
        print(action)

        # LangGraph nodes must return a dict of state updates. Here we pass
        # most fields through unchanged, but set "finished" based on whether
        # the planner said we are done (action == "FINISH").
        return {
            "actions": state["actions"],
            "observations": state["observations"],
            "current_step": state["current_step"],
            "finished": action == "FINISH",
            "final_answer": state["final_answer"]
        }

    return planner_node


def build_graph(tools):
    # Create a new graph whose state will follow the AgentState schema.
    builder = StateGraph(AgentState)

    # Build the actual node function, bound to the tools available to it.
    planner_node = create_planner_node(tools)

    # Register the node under the name "planner" so edges can reference it.
    builder.add_node(
        "planner",
        planner_node
    )

    # START -> planner: the graph begins by running the planner node.
    builder.add_edge(
        START,
        "planner"
    )

    # planner -> END: after planning once, the graph finishes (no looping
    # or conditional routing in this "basic graph" lesson).
    builder.add_edge(
        "planner",
        END
    )

    # Compile turns the builder definition into a runnable graph object.
    return builder.compile()

