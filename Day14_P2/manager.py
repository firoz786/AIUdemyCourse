from openai import OpenAI
from dotenv import load_dotenv
import os

from research_agent import research
from coding_agent import write_code
from reviewer_agent import review
from state import create_state


load_dotenv()


client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def choose_worker(state):

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
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

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

    state = create_state(
        task
    )

    while True:

        worker = choose_worker(
            state
        )

        print(
            f"\nManager selected: {worker}"
        )

        if worker == "research":

            state["research"] = research(
                state["task"]
            )

            state["history"].append(
                "research"
            )

        elif worker == "coding":

            state["code"] = write_code(
                state["task"],
                state["research"]
            )

            state["history"].append(
                "coding"
            )

        elif worker == "review":

            state["review"] = review(
                state["task"],
                state["code"]
            )

            state["history"].append(
                "review"
            )

        elif worker == "finish":

            break

        else:

            raise ValueError(
                f"Unknown worker: {worker}"
            )

    return state

