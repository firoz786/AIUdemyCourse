from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


MODEL = "qwen3:1.7b"


def rerank(
    query,
    candidates,
    top_k=3
):

    scored = []

    for candidate in candidates:

        prompt = f"""
You are a document relevance evaluator.

User Query:
{query}

Document:
{candidate["text"]}

Give a relevance score from 0 to 100.

100 = directly answers the query
0 = completely irrelevant

Return ONLY the number.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        score_text = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        try:
            score = float(score_text)
        except ValueError:
            score = 0

        scored.append({
            **candidate,
            "rerank_score": score
        })

    scored.sort(
        key=lambda item:
        item["rerank_score"],
        reverse=True
    )

    return scored[:top_k]


