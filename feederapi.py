import os
import sys
# @title Get TradingView Data as POST API
from flask import Flask, request, jsonify
from tvDatafeeds import TvDatafeed, Interval

app = Flask(__name__)

def convert_interval(interval_str):
    """Convert string interval to Interval object"""
    if interval_str == "1m":
        return Interval.in_1_minute
    elif interval_str == "3m":
        return Interval.in_3_minute
    elif interval_str == "5m":
        return Interval.in_5_minute
    elif interval_str == "30m":
        return Interval.in_30_minute
    elif interval_str == "45m":
        return Interval.in_45_minute
    elif interval_str == "1h":
        return Interval.in_1_hour
    elif interval_str == "2h":
        return Interval.in_2_hour
    elif interval_str == "3h":
        return Interval.in_3_hour
    elif interval_str == "4h":
        return Interval.in_4_hour
    elif interval_str == "d":
        return Interval.in_daily
    elif interval_str == "w":
        return Interval.in_weekly
    elif interval_str == "M":
        return Interval.in_monthly
    else:
        return Interval.in_1_hour

@app.route('/api/data', methods=['POST'])
def get_tradingview_data():
    try:
        # Parse request body
        req_data = request.get_json()

        # Check if request body is provided
        if not req_data:
            return jsonify({
                'error': 'Request body is missing or not in JSON format'
            }), 400

        # Extract parameters from request body
        symbol = req_data.get('Symbol', 'XMRUSDT')
        exchange = req_data.get('Exchange', 'KUCOIN')
        bars = req_data.get('Bars', 1000)
        interval_str = req_data.get('Interval', '1m')

        # Validate required parameters
        if not symbol:
            return jsonify({
                'error': 'Symbol is required'
            }), 400

        if not exchange:
            return jsonify({
                'error': 'Exchange is required'
            }), 400

        if not bars:
            return jsonify({
                'error': 'Bars is required'
            }), 400

        if not interval_str:
            return jsonify({
                'error': 'Interval is required'
            }), 400

        # Validate that bars is a positive integer
        if not isinstance(bars, int) or bars <= 0:
            return jsonify({
                'error': 'Bars must be a positive integer'
            }), 400

        # Convert interval string to Interval object
        interval = convert_interval(interval_str)

        # Fetch data from TradingView
        tv = TvDatafeed()
        data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=bars)

        # Convert DataFrame to JSON serializable format
        result = {
            'symbol': symbol,
            'exchange': exchange,
            'interval': interval_str,
            'bars': bars,
            'data': data.reset_index().to_dict('records')  # Convert DataFrame to list of dictionaries
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)