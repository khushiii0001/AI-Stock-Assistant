import json
import os

from groq import Groq

from tools import (
    TOOLS,
    TOOLS_SCHEMA
)

MODEL = "llama-3.3-70b-versatile"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_agent(question):

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:

        function_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        result = TOOLS[
            function_name
        ](**arguments)

        messages.append(message)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        )

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return final_response.choices[0].message.content