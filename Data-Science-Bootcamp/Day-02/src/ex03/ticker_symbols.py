import sys


def get_stock_data():
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    
    return COMPANIES, STOCKS

def lookup_by_ticker(ticker_symbol):
    COMPANIES, STOCKS = get_stock_data()

    if ticker_symbol in STOCKS:
        stock_price = STOCKS[ticker_symbol]
        company_name = None
        for company, ticker in COMPANIES.items():
            if ticker == ticker_symbol:
                company_name = company
                break
        return company_name, stock_price
    else:
        return None, None


def main():
    if len(sys.argv) != 2:
        return
    
    ticker_symbol = sys.argv[1].upper()
    company_name, stock_price = lookup_by_ticker(ticker_symbol)

    if company_name is not None and stock_price is not None:
        print(f"{company_name} {stock_price}")
    else:
        print("Unknown ticker")

if __name__ == '__main__':
    main()