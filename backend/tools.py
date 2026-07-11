from stock_tools import (
    get_stock_price,
    get_fundamentals,
    get_news
)

TOOLS = {
    "get_stock_price": get_stock_price,
    "get_fundamentals": get_fundamentals,
    "get_news": get_news
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get current stock price",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string"
                    }
                },
                "required": ["ticker"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_fundamentals",
            "description": "Get PE ratio, market cap, revenue and sector",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string"
                    }
                },
                "required": ["ticker"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Get latest stock news",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string"
                    }
                },
                "required": ["ticker"]
            }
        }
    }
]