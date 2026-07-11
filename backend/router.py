import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

MODEL = "llama-3.3-70b-versatile"

ROUTER_PROMPT = """
You are a routing agent.

Available tools:

price_tool
fundamental_tool
news_tool
portfolio_tool

Use these rules:

price_tool:
- current price
- stock price
- trading price
- latest price

fundamental_tool:
- PE ratio
- market cap
- revenue
- sector
- fundamentals

news_tool:
- news
- latest updates
- recent developments
- headlines

portfolio_tool:
- portfolio value
- my holdings
- my profit
- portfolio profit
- best performing stock
- top performing stock
- portfolio summary
- portfolio allocation

If a question requires multiple tools,
return all required tools.

Rules:
- For portfolio-only questions, do NOT return a ticker.
- For stock-specific questions, return ticker.
- Return ONLY valid JSON.

Examples:

Question:
What is TCS PE ratio?

Output:
{
  "tools":["fundamental_tool"],
  "ticker":"TCS.NS"
}

Question:
Show latest Infosys news

Output:
{
  "tools":["news_tool"],
  "ticker":"INFY.NS"
}

Question:
Compare TCS PE ratio and latest news

Output:
{
  "tools":["fundamental_tool","news_tool"],
  "ticker":"TCS.NS"
}

Question:
Give me current price and PE ratio of Reliance

Output:
{
  "tools":["price_tool","fundamental_tool"],
  "ticker":"RELIANCE.NS"
}

Question:
What is my portfolio value?

Output:
{
  "tools":["portfolio_tool"]
}

Question:
Which stock is giving me highest profit?

Output:
{
  "tools":["portfolio_tool"]
}

Question:
Show my portfolio summary

Output:
{
  "tools":["portfolio_tool"]
}

Question:
Show my portfolio value and latest TCS news

Output:
{
  "tools":["portfolio_tool","news_tool"],
  "ticker":"TCS.NS"
}


Return ONLY JSON.
"""

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def route(question, history=None):

    if history is None:
        history = []

    messages = [
        {
            "role":"system",
            "content":ROUTER_PROMPT
        }
    ]

    messages.extend(history[-10:])

    messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=messages
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        if content.startswith("json"):
            content = content[4:].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"tools": [], "ticker": None}