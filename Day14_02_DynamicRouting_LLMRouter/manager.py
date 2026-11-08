"""
Day 14.02 - Dynamic Routing with an LLM Router: Manager
-------------------------------------------------------------
What's NEW in this file compared to Day 14.01: instead of hardcoding the
order "research -> coding -> review", the Manager now asks the LLM itself
(`choose_worker`) which worker should run next, based on the current
shared `state` (see state.py). This is a simple but real example of
"dynamic routing" - the control flow is decided by the model, not by
fixed Python code. The Manager loops, calling `choose_worker` after every
step, until the LLM says "finish".
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
    # Build a prompt that turns the Manager into a pure "router": it only
    # looks at which fields of the state are empty/non-empty and returns the
    # single next action, without doing any of the actual work itself.
    prompt = f"""
You are the Manager Agent in a multi-agent system.

Your ONLY responsibility is to decide which worker should execute NEXT
based on the current state.

Do NOT perform the task yourself.
Do NOT explain your reasoning.
Do NOT generate code.
Do NOT generate research.
Do NOT review anything.

========================
ORIGINAL TASK
========================
{state["task"]}

========================
CURRENT STATE
========================

Research:
{state["research"]}

Code:
{state["code"]}

Review:
{state["review"]}

Execution History:
{state["history"]}

========================
AVAILABLE ACTIONS
========================

research
coding
review
finish

========================
DECISION RULES
========================

Follow these rules EXACTLY and in this order:

1. If Research is empty:
   return research

2. Otherwise, if Code is empty:
   return coding

3. Otherwise, if Review is empty:
   return review

4. Otherwise:
   return finish

IMPORTANT:
- Never select research when Research is already available.
- Never select coding when Code is already available.
- Never select review when Review is already available.
- Never select finish if Research, Code, or Review is empty.
- Do not consider the contents of the fields when deciding whether
  they are complete. Only check whether they are empty or non-empty.
- The Execution History is informational only. The current state has
  higher priority.

========================
OUTPUT FORMAT
========================

Return EXACTLY ONE word.

Valid outputs are:

research
coding
review
finish

Do not return:
- explanations
- sentences
- markdown
- backticks
- punctuation
- additional words

Example:
review
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
    result = (
        response
        .choices[0]
        .message
        .content
        .strip()
        .lower()
    )
    return result


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
            # Call the Coding Agent using the task and the research notes.
            state["code"] = write_code(
                state["task"],
                state["research"]
            )

            state["history"].append(
                "coding"
            )

        elif worker == "review":
            # Call the Reviewer Agent to critique the generated code.
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

