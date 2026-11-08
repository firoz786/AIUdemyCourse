"""
Day 14.03 - Review Loop with Structured Feedback: Manager
-------------------------------------------------------------
What's NEW in this file compared to Day 14.02: the Reviewer Agent now
returns structured JSON (status + feedback, see reviewer_agent.py), so the
Manager's routing rules can check `state["review"]["status"]` and send the
code back to the Coding Agent ("needs_revision") along with the specific
feedback to fix, instead of only checking whether a review exists at all.
This creates a real "review loop": coding -> review -> coding -> review...
"""

# Official OpenAI SDK client - used by choose_worker() to ask the router question.
from openai import OpenAI
# Loads key/value pairs from a local .env file into environment variables.
from dotenv import load_dotenv
# Standard library module used to read those environment variables.
import os

# Import the three worker agents this manager coordinates.
from research_agent import research
from coding_agent import write_code
from reviewer_agent import review
# Import the helper that builds the initial shared state dictionary.
from state import create_state


# Read the .env file now so os.getenv() calls below can find BASE_URL / API_KEY / MODEL.
load_dotenv()


# Create one shared OpenAI client for this module, configured from environment
# variables so the same code can point at OpenAI or any OpenAI-compatible endpoint.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def choose_worker(state):
    # Build a prompt that turns the Manager into a router: it looks at the
    # current state (including the structured review status) and returns
    # only the name of the next worker to run.
    prompt = f"""
You are the Manager Agent.

Your job is to decide which worker
should act NEXT.

Original Task:
{state["task"]}

Research:
{state["research"]}

Code:
{state["code"]}

Review:
{state["review"]}

History:
{state["history"]}

Available workers:

research
coding
review
finish

Decision rules:

- If research is empty, choose research.

- If research exists and code is empty,
  choose coding.

- If a review exists with status
  "needs_revision", choose coding.

- If code exists and there is no review,
  choose review.

- If the previous review requested
  revision and new code has been generated,
  choose review again.

- If the latest review status is
  "approved", choose finish.

Return ONLY one word:

research
coding
review
finish
"""
    # Ask the LLM to pick the next worker.
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Normalize the reply (strip whitespace, lowercase) so comparisons like
    # `worker == "research"` below are reliable even with minor formatting noise.
    return (
        response
        .choices[0]
        .message
        .content
        .strip()
        .lower()
    )


def run_manager(task):
    # Create the starting state: task filled in, everything else empty.
    state = create_state(
        task
    )

    # Keep asking the router "what's next?" until it says "finish".
    while True:

        worker = choose_worker(
            state
        )

        print(
            f"\nManager selected: {worker}"
        )

        if worker == "research":
            # Call the Research Agent and store its output in the state.
            state["research"] = research(
                state["task"]
            )

            state["history"].append(
                "research"
            )

        elif worker == "coding":
            # Pull the feedback text out of the previous structured review
            # (if one exists) so the Coding Agent knows what to fix.
            feedback = ""

            if state["review"]:

                feedback = state[
                    "review"
                ].get(
                    "feedback",
                    ""
                )

            # Call the Coding Agent, passing along any reviewer feedback.
            state["code"] = write_code(
                state["task"],
                state["research"],
                feedback
            )

            state["history"].append(
                "coding"
            )

        elif worker == "review":
            # Call the Reviewer Agent, which returns a structured
            # {"status": ..., "feedback": ...} dictionary.
            state["review"] = review(
                state["task"],
                state["code"]
            )

            state["history"].append(
                "review"
            )

        elif worker == "finish":
            # The router says the pipeline is complete - stop looping.
            break

        else:
            # Defensive check: the LLM returned something unexpected.
            raise ValueError(
                f"Unknown worker: {worker}"
            )

    return state

