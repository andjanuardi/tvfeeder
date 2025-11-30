# TV Feed API - TradingView Data Fetcher

## Project Overview

TV Feed API is a cryptocurrency data fetching service that provides a REST API interface for retrieving historical price data from TradingView. The project is built with Flask and uses a custom version of the tvdatafeed library to fetch data from TradingView for various symbols and exchanges.

The project is designed to fetch historical price data for cryptocurrency pairs (such as XMRUSDT) and other financial instruments against various exchanges from TradingView, then serve this data via a simple REST API endpoint.

## Project Structure

The project consists of the following files:

- `feederapi.py`: Main Flask API application that serves as the TradingView data endpoint
- `requirements.txt`: Python dependencies for the project
- `tvdatafeed/`: Local clone of the tvdatafeed repository from GitHub, modified to include live data retrieving features
- `QWEN.md`: Project documentation (this file)

## Dependencies

The project requires the following Python packages:
- flask: Web framework for creating the API server
- tvdatafeed: TradingView data fetching library (forked version with live data feature)
- setuptools: Python package development and distribution tools
- pandas: Data manipulation and analysis library
- websocket-client: WebSocket client for Python
- requests: HTTP library for Python

## API Endpoint

### `/api/data` (POST)

The main endpoint accepts a JSON payload with the following parameters:

- `Symbol` (string): Trading symbol to fetch data for (e.g. 'XMRUSDT', default: 'XMRUSDT')
- `Exchange` (string): Exchange to fetch data from (e.g. 'KUCOIN', default: 'KUCOIN')
- `Bars` (integer): Number of data bars to retrieve (default: 1000, must be positive)
- `Interval` (string): Time interval for the data (default: '1m')

Supported intervals:
- '1m', '3m', '5m', '15m', '30m', '45m', '1h', '2h', '3h', '4h', 'd', 'w', 'M'

Example request:
```json
{
  "Symbol": "BTCUSDT",
  "Exchange": "BINANCE",
  "Bars": 500,
  "Interval": "1h"
}
```

The API returns a JSON response with the symbol, exchange, interval, number of bars, and the historical data in a list of dictionaries format.

## Building and Running

### Installation
1. Install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

### Running the API Server
1. Execute the `feederapi.py` script to start the Flask server:
   ```
   python feederapi.py
   ```

2. The server will start on `http://0.0.0.0:5000` by default
3. Send POST requests to `/api/data` to fetch TradingView data

## Configuration

The API currently runs on port 5000 and accepts connections from any host (0.0.0.0).
The tvdatafeed library can be used with or without login credentials, though using without login may limit available data for some symbols.

## tvdatafeed Library

This project uses a fork of the original tvdatafeed library by StreamAlpha, which has been enhanced with live data retrieving features. The library provides access to TradingView's historical market data without requiring a premium subscription.

The library supports:
- Fetching up to 5000 bars on any supported timeframe
- Various exchange and symbol combinations
- Live data feed functionality (though not currently used in the API)
- Multiple interval options from 1 minute to monthly

## Project Purpose

This project is designed to provide a simple REST API interface to fetch historical cryptocurrency and financial instrument price data from TradingView for analysis, backtesting strategies, or integration into other applications that require market data.

## Local Development

The project uses a local clone of the tvdatafeed repository, allowing for:
- Direct access to the library source code
- Ability to modify the library behavior if needed
- Testing changes to the library without affecting other projects
- Integration of live data features if needed in the future