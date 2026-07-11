import yfinance as yf


def get_stock_price(ticker):
    stock = yf.Ticker(ticker)

    return {
        "symbol": ticker,
        "price": stock.info.get("currentPrice")
    }

def get_fundamentals(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "sector": info.get("sector"),
        "revenue": info.get("totalRevenue")
    }

def get_news(ticker):

    stock = yf.Ticker(ticker)

    news = stock.news
    if not news:
        return {
            "message": f"No news found for {ticker}"
        }

    return news[:5]    

if __name__ == "__main__":
    print(get_news("CUPID.NS"))    