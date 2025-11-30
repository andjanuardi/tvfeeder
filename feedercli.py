import json
import sys
import argparse
import pandas as pd
from datetime import datetime

# Add the tvdatafeed package directory to the Python path
from tvDatafeed import TvDatafeed, Interval


def get_interval_from_string(interval_str):
    """Map string interval to TvDatafeed Interval object."""
    interval_map = {
        '1m': Interval.in_1_minute,
        '3m': Interval.in_3_minute,
        '5m': Interval.in_5_minute,
        '15m': Interval.in_15_minute,
        '30m': Interval.in_30_minute,
        '45m': Interval.in_45_minute,
        '1h': Interval.in_1_hour,
        '2h': Interval.in_2_hour,
        '3h': Interval.in_3_hour,
        '4h': Interval.in_4_hour,
        'd': Interval.in_daily,
        'w': Interval.in_weekly,
        'M': Interval.in_monthly
    }

    interval_str = interval_str.lower().replace(' ', '')
    if interval_str not in interval_map:
        raise ValueError(f"Invalid interval: {interval_str}. Supported intervals: {', '.join(interval_map.keys())}")

    return interval_map[interval_str]


def main():
    parser = argparse.ArgumentParser(description='Fetch historical market data from TradingView')
    parser.add_argument('--symbol',dest='symbol', type=str, help='Trading symbol (e.g. XMRUSDT)',default="XMRUSDT",nargs='?')
    parser.add_argument('--exchange',dest='exchange', type=str, help='Exchange name (e.g. KUCOIN)',default="KUCOIN",nargs='?')
    parser.add_argument('--interval',dest='interval', type=str, help='Time interval (e.g. 5m, 1h, d)',default="4h",nargs='?')
    parser.add_argument('--bars',dest='bars', type=int, help='Number of bars to fetch', default=1000,nargs='?')
    parser.add_argument('--json', type=str, help='Output JSON file name', dest='json_file')

    args = parser.parse_args()


    # Validate arguments
    if args.bars <= 0:
        print(json.dumps({"error": "Number of bars must be greater than 0"}), file=sys.stderr)
        sys.exit(1)

    try:
        interval = get_interval_from_string(args.interval)
    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    # Initialize TV data feed
    tv = TvDatafeed()

    try:
        # Fetch the data
        data = tv.get_hist(symbol=args.symbol, exchange=args.exchange, interval=interval, n_bars=args.bars)

        # Convert DataFrame to JSON serializable format
        df_reset = data.reset_index()

        # Convert Timestamps to string format to make them JSON serializable
        for col in df_reset.columns:
            if df_reset[col].dtype == 'datetime64[ns]' or col == 'datetime':
                df_reset[col] = df_reset[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Convert to dictionary
        data_json = df_reset.to_dict(orient='records')

        # Create output with metadata
        output = {
            "info": {
                "Symbol": args.symbol,
                "Exchange": args.exchange,
                "Timeframe": args.interval
            },
            "data": data_json
        }

        # Output JSON to file if specified
        if args.json_file:
            with open(args.json_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"Data successfully written to {args.json_file}", file=sys.stderr)
        else:
            # Print JSON output to stdout
            print(json.dumps(output))

    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch data: {str(e)}"}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()