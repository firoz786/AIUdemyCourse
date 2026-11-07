from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()


client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def write_code(
    task,
    research
):

    prompt = f"""
You are a Coding Agent.

Write Python code based on the task
and research.

Task:
{task}

Research:
{research}

Return:

1. Short explanation
2. Complete Python code
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

    return response.choices[0].message.content
