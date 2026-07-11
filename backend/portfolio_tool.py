import sqlite3
import yfinance as yf


DB_NAME = "portfolio.db"


def get_holdings():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT ticker, quantity, buy_price
    FROM portfolio
    """)

    rows = cursor.fetchall()

    conn.close()

    holdings = []

    for row in rows:

        holdings.append({
            "ticker": row[0],
            "quantity": row[1],
            "buy_price": row[2]
        })

    return holdings

    def get_portfolio_value():

    holdings = get_holdings()

    total_value = 0

    positions = []

    for holding in holdings:

        ticker = holding["ticker"]

        stock = yf.Ticker(ticker)

        current_price = stock.info.get("currentPrice")

        quantity = holding["quantity"]

        position_value = current_price * quantity

        total_value += position_value

        positions.append({
            "ticker": ticker,
            "current_price": current_price,
            "quantity": quantity,
            "value": round(position_value, 2)
        })

    return {
        "total_value": round(total_value, 2),
        "positions": positions
    }

    def get_portfolio_profit():

    holdings = get_holdings()

    total_profit = 0

    results = []

    for holding in holdings:

        ticker = holding["ticker"]

        quantity = holding["quantity"]

        buy_price = holding["buy_price"]

        stock = yf.Ticker(ticker)

        current_price = stock.info.get("currentPrice")

        profit = (
            current_price - buy_price
        ) * quantity

        total_profit += profit

        results.append({
            "ticker": ticker,
            "buy_price": buy_price,
            "current_price": current_price,
            "profit": round(profit, 2)
        })

    return {
        "total_profit": round(total_profit, 2),
        "holdings": results
    }

    def best_performer():

    holdings = get_holdings()

    best_stock = None

    highest_profit = float("-inf")

    for holding in holdings:

        ticker = holding["ticker"]

        quantity = holding["quantity"]

        buy_price = holding["buy_price"]

        stock = yf.Ticker(ticker)

        current_price = stock.info.get("currentPrice")

        profit = (
            current_price - buy_price
        ) * quantity

        if profit > highest_profit:

            highest_profit = profit

            best_stock = ticker

    return {
        "ticker": best_stock,
        "profit": round(highest_profit, 2)
    }

    def get_portfolio_summary():

    return {
        "portfolio_value":
            get_portfolio_value(),

        "portfolio_profit":
            get_portfolio_profit(),

        "best_performer":
            best_performer()
    }

    

