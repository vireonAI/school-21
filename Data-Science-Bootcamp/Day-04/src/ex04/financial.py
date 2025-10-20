#!/usr/bin/env python3  
from bs4 import BeautifulSoup
import requests
import sys

def fetch_financial_page(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",  
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    response = requests.get(url, headers=headers)
    
    
    if response.status_code != 200:
        raise Exception(f"URL for ticker '{ticker}' does not exist. Status code: {response.status_code}")
    
    return response.text

def parse_financial_table(html, field):
    soup = BeautifulSoup(html, 'html.parser')
    table_section = soup.find("section", {"data-testid": "qsp-financials"})
    
    if not table_section:
        raise Exception("Financial table not found in the page.")
    
    rows = table_section.find_all("div", class_="row lv-0 yf-t22klz")
    if not rows:
        raise Exception("No rows found in financial table.")
    
    for row in rows:
        label = row.find("div", class_="rowTitle").get_text(strip=True)
        if label.lower() == field.lower():

            all_cols = row.find_all("div", class_="column yf-t22klz") + \
                       row.find_all("div", class_="column yf-t22klz alt")
            values = [col.get_text(strip=True) for col in all_cols]
            return tuple([label] + values)
    
    raise Exception(f"Field '{field}' not found in financial table.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 financial.py <TICKER> <FIELD>")
        sys.exit(1)
    
    ticker = sys.argv[1]
    field = sys.argv[2]
    
    try:
        html = fetch_financial_page(ticker)
        result = parse_financial_table(html, field)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
