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
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
        .strip()
        .lower()
    )


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

            feedback = ""

            if state["review"]:

                feedback = state[
                    "review"
                ].get(
                    "feedback",
                    ""
                )

            state["code"] = write_code(
                state["task"],
                state["research"],
                feedback
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

