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

def lookup_stock_price(company_name):
    COMPANIES, STOCKS = get_stock_data()
    
    if company_name in COMPANIES:
        stock_symbol = COMPANIES[company_name]
        stock_price = STOCKS[stock_symbol]
        return stock_price
    else:
        return None


def main():
    if len(sys.argv) != 2:
        return
    
    company_name = sys.argv[1].capitalize()
    stock_price = lookup_stock_price(company_name)
    
    if stock_price is not None:
        print(stock_price)
    else:
        print("Unknown company")


if __name__ == '__main__':
    main()