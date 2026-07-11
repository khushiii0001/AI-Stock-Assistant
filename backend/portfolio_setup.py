import sqlite3

conn = sqlite3.connect("portfolio.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    buy_price REAL NOT NULL
)
""")

sample_data = [
    ("TCS.NS", 10, 3200),
    ("RELIANCE.NS", 20, 1400),
    ("INFY.NS", 15, 1500),
]

cursor.executemany(
    """
    INSERT INTO portfolio
    (ticker, quantity, buy_price)
    VALUES (?, ?, ?)
    """,
    sample_data
)

conn.commit()
conn.close()

print("portfolio.db created")