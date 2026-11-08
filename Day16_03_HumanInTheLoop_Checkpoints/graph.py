"""
Day 16.03 - Human-in-the-Loop Checkpoints (LangGraph).

This module builds a LangGraph state machine that implements a simple
"plan -> ask human -> act -> answer" agent loop. The key teaching concept
here is `interrupt()` combined with a checkpointer (`InMemorySaver`): the
graph can pause itself mid-run to ask a human for approval before running a
tool, and later resume exactly where it left off once the human responds.
This is the core pattern behind "human-in-the-loop" AI agents.
"""

# Core LangGraph building blocks: StateGraph is the graph builder, START/END
# are the special entry/exit node markers.
from langgraph.graph import (
    StateGraph,
    START,
    END
)

# interrupt() pauses graph execution and hands control back to the caller
# (e.g. to ask a human a question) until the graph is resumed.
from langgraph.types import interrupt

# InMemorySaver is a checkpointer: it stores the graph's state in memory so
# that execution can be paused (via interrupt) and resumed later.
from langgraph.checkpoint.memory import (
    InMemorySaver
)

# Our own building blocks: decides the next action, runs a tool, and
# formats the final natural-language answer.
from agent.planner import planner
from agent.executor import execute_action
from agent.runner import format_answer

# The shared state shape (a TypedDict) that flows between every node.
from agent.state import AgentState


def create_planner_node(tools):
    """Factory that returns a graph node which asks the LLM planner what to do next."""

    def planner_node(state: AgentState):
        # Ask the planner (an LLM call) which tool to run next, or "FINISH".
        action = planner(state, tools)

        print("\nPlanner Selected:")
        print(action)

        # Update the shared state with the chosen action and whether we're done.
        return {
            "action": action,
            "finished": action == "FINISH"
        }

    return planner_node


def approval_node(state: AgentState):
    """Pause the graph and ask a human to approve the selected tool call."""

    # interrupt() freezes execution here and returns control to the caller
    # (main.py), passing along this payload for the human to review.
    decision = interrupt(
        {
            "message": "Approve this tool call?",
            "action": state["action"]
        }
    )

    # When the graph is resumed, `decision` contains whatever the human replied.
    return {
        "approval": decision
    }


def create_tool_node(client):
    """Factory that returns a graph node which actually executes the approved tool."""

    async def tool_node(state: AgentState):
        action = state["action"]

        # Run the approved tool against the MCP client and get its result text.
        observation = await execute_action(action, state, client)

        print("\nTool Observation:")
        print(observation)

        # Append this step's action/observation to the running history and
        # advance the step counter, so the planner can see progress so far.
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


def answer_node(state: AgentState):
    """Turn the collected actions/observations into a final natural-language answer."""

    answer = format_answer(state)

    print("\nFinal Answer:")
    print(answer)

    return {
        "final_answer": answer,
        "finished": True
    }


def route_after_planner(state: AgentState):
    """Decide which node runs after the planner: ask for approval, or finish."""

    if state["action"] == "FINISH":
        return "finish"

    return "approval"


def route_after_approval(state: AgentState):
    """Decide which node runs after the human responds: run the tool, or skip it."""

    if state["approval"] == "yes":
        return "approved"

    return "rejected"


def route_after_tool(state: AgentState):
    """Decide whether to loop back to the planner or stop once max_steps is hit."""

    if state["current_step"] >= state["max_steps"]:
        return "stop"

    return "continue"


def build_graph(tools, client):
    """Wire all nodes and edges together into a compiled, runnable LangGraph."""

    builder = StateGraph(AgentState)

    # Register each node (a plain function) under a name used by the edges below.
    builder.add_node("planner", create_planner_node(tools))
    builder.add_node("approval", approval_node)
    builder.add_node("tool", create_tool_node(client))
    builder.add_node("answer", answer_node)

    # Every run starts at the planner node.
    builder.add_edge(START, "planner")

    # After planning: go ask for approval, unless the planner said FINISH.
    builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "approval": "approval",
            "finish": "answer"
        }
    )

    # After the human responds: run the tool if approved, otherwise skip to the answer.
    builder.add_conditional_edges(
        "approval",
        route_after_approval,
        {
            "approved": "tool",
            "rejected": "answer"
        }
    )

    # After running a tool: keep looping (back to planner) or stop if max_steps reached.
    builder.add_conditional_edges(
        "tool",
        route_after_tool,
        {
            "continue": "planner",
            "stop": "answer"
        }
    )

    # Once we reach the answer node, the graph run is complete.
    builder.add_edge("answer", END)

    # The checkpointer is what makes interrupt()/resume possible: it persists
    # state between the pause and the later resume call.
    checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)
