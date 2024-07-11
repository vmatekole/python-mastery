from rich import print

tickers = ['HPQ', 'AA', 'AAPL', 'AIG', 'YHOO', 'GOOG', 'RHT']

ticker_str = ''.join(tickers)

print(ticker_str.index('AAPL'))

try:
    tickers.remove('A')
except Exception as e:
    print(f"Exception: {e}")

print(tickers)


prices = {'CASIO': 10.2, 'IBM': 19.1, 'APPLE': 23.1, 'CASIO': 40.2}

print(f"Prices as dict: {prices}")
print(f"Prices as a list: {list(prices)}")
print(f"Prices as a set: {set(prices)}")
