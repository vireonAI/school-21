import sys


def get_stock_data():
    """
    data
    """
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


def normalize_string(text):
    return text.strip()


def find_company_by_ticker(ticker, companies_dict):
    for company, company_ticker in companies_dict.items():
        if company_ticker.upper() == ticker.upper():
            return company
    return None


def process_expression(expression):
    COMPANIES, STOCKS = get_stock_data()
    
    normalized_expr = normalize_string(expression)
    
    if not normalized_expr:  
        return None
    
    companies_lower = {k.lower(): k for k in COMPANIES.keys()}
    stocks_upper = {k.upper(): k for k in STOCKS.keys()}
    
    expr_lower = normalized_expr.lower()
    if expr_lower in companies_lower:
        original_company_name = companies_lower[expr_lower]
        ticker = COMPANIES[original_company_name]
        stock_price = STOCKS[ticker]
        return f"{original_company_name} stock price is {stock_price}"
    
    expr_upper = normalized_expr.upper()
    if expr_upper in stocks_upper:
        original_ticker = stocks_upper[expr_upper]
        company_name = find_company_by_ticker(original_ticker, COMPANIES)
        return f"{original_ticker} is a ticker symbol for {company_name}"
    
    return f"{normalized_expr} is an unknown company or an unknown ticker symbol"


def check_for_empty_expressions(expressions_list):
    for expr in expressions_list:
        if normalize_string(expr) == "":
            return True
    return False


def main():
    if len(sys.argv) != 2:
        return
    
    input_string = sys.argv[1]
    expressions = input_string.split(',')
    
    if check_for_empty_expressions(expressions):
        return
    
    results = []
    for expression in expressions:
        result = process_expression(expression)
        if result is not None:
            results.append(result)
    
    for result in results:
        print(result)


if __name__ == '__main__':
    main()