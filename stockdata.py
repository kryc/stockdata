import argparse
from datetime import datetime, timedelta, timezone
import math
import requests
import sys
from typing import Tuple

def get_stock_data(ticker: str, period: Tuple[int, int]) -> str:
    #https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1=1644395365&period2=1675931365&interval=1d&events=history&includeAdjustedClose=true
    url = (
        f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?'
        f'period1={period[0]}&period2={period[1]}&interval=1d&'
        'events=history&includeAdjustedClose=true'
    )
    headers ={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }
    req = requests.get(url, headers=headers, timeout=1000)
    return req.text

def get_timestamps(years: int, round_down: bool = True) -> Tuple[int, int]:
    end_date = datetime.now(tz=timezone.utc)
    delta = timedelta(days=365*years)
    start_date = end_date - delta
    if round_down:
        start_date = datetime(start_date.year, 1, 1)
    stamp_start = math.floor(datetime.timestamp(start_date))
    stamp_end = math.floor(datetime.timestamp(end_date))
    return (stamp_start, stamp_end,)

def dump(ticker: str, format: str, output: str) -> None:
    timestamps = get_timestamps(10)
    stock_data = get_stock_data(ticker, timestamps)
    if output == '-':
        print(stock_data)
    else:
        with open(output, 'wt', encoding='utf8') as fh:
            fh.write(stock_data)

def main() -> None:
    parser = argparse.ArgumentParser(description='Gather and process stock data')
    parser.add_argument('mode', choices=('dump',), help='Operating mode')
    args = parser.parse_args(sys.argv[1:2])

    if args.mode == 'dump':
        parser = argparse.ArgumentParser(description='Dump ticker information')
        parser.add_argument('ticker', help='Ticker symbol')
        parser.add_argument('format', choices=('csv',), help='Output format')
        parser.add_argument('output', help='Destination file (or "-" for stdout')
        args = parser.parse_args(sys.argv[2:])
        return dump(args.ticker, args.format, args.output)

if __name__ == '__main__':
    main()