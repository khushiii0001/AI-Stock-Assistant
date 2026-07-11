import json
import os
from concurrent.futures import ThreadPoolExecutor

from groq import Groq

from router import route
from stock_tools import (
    get_stock_price,
    get_fundamentals,
    get_news
)

MODEL = "llama-3.3-70b-versatile"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

ANSWER_PROMPT = """
You are a stock market assistant.

Format responses in markdown.

For fundamentals use:

## Fundamentals

- Market Cap:
- PE Ratio:
- Revenue:
- Sector:

For news:

## Latest News

- Headline 1
- Headline 2

For prices:

## Current Price

₹1234

Never return raw JSON.
Never return one-line answers if more details exist.
"""

def execute_tools(tools, ticker):
    """
    Execute multiple tools in parallel.
    """

    results = {}

    with ThreadPoolExecutor(max_workers=5) as executor:

        futures = {}

        for tool in tools:

            if tool == "price_tool":
                futures["price"] = executor.submit(
                    get_stock_price,
                    ticker
                )

            elif tool == "fundamental_tool":
                futures["fundamentals"] = executor.submit(
                    get_fundamentals,
                    ticker
                )

            elif tool == "news_tool":
                futures["news"] = executor.submit(
                    get_news,
                    ticker
                )

        for key, future in futures.items():
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = {
                    "error": str(e)
                }

    return results


def ask_agent(question, history=None):

    if history is None:
        history = []

    route_result = route(question, history) or {}

    tools = route_result.get("tools", [])
    ticker = route_result.get("ticker")

    if not tools:
        yield "I don't have enough information."
        return

    tool_results = execute_tools(
        tools,
        ticker
    )

    context = json.dumps(
        tool_results,
        indent=2,
        default=str
    )

    messages = [
        {
            "role": "system",
            "content": ANSWER_PROMPT
        }
    ]

    # Add previous conversation
    messages.extend(history[-10:])

    # Add current question + tool results
    messages.append(
        {
            "role": "user",
            "content": f"""
Question:
{question}

Tool Results:
{context}
"""
        }
    )

    print("\n===== HISTORY =====")
    print(messages)

    stream = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        stream=True,
        messages=messages
    )

    for chunk in stream:

        delta = chunk.choices[0].delta.content

        if delta:
            yield delta
