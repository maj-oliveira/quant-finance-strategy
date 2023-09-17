import yfinance as yf

def main() -> None:
    data = yf.download('AAPL',start='2021-01-01',end='2023-01-01')
    print(data.head())

if __name__ == '__main__':
    main()