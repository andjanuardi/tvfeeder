# TV Feed API - TradingView Data Fetcher

TV Feed API is a cryptocurrency data fetching service that provides a REST API interface for retrieving historical price data from TradingView. The project is built with Flask and uses a custom version of the tvdatafeed library to fetch data from TradingView for various symbols and exchanges.

## Features

- REST API endpoint for fetching TradingView historical data
- Support for multiple exchanges and trading symbols
- Configurable time intervals from 1 minute to monthly
- Easy-to-use JSON-based request/response format
- Built with Flask for simple deployment and scaling

## Dependencies

- Python 3.7+
- Flask
- tvdatafeed (custom fork with live data feature)
- pandas
- websocket-client
- requests

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/tvfeed-api.git
   cd tvfeed-api
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the API server:
   ```bash
   python feederapi.py
   ```

2. The server will start on `http://localhost:5000`

3. Send POST requests to `/api/data` with JSON payload like:
   ```json
   {
     "Symbol": "BTCUSDT",
     "Exchange": "BINANCE",
     "Bars": 500,
     "Interval": "1h"
   }
   ```

## API Endpoint

### POST `/api/data`

Fetches historical data from TradingView.

**Request Body Parameters:**
- `Symbol` (string): Trading symbol to fetch data for (e.g. 'XMRUSDT', default: 'XMRUSDT')
- `Exchange` (string): Exchange to fetch data from (e.g. 'KUCOIN', default: 'KUCOIN')
- `Bars` (integer): Number of data bars to retrieve (default: 1000, must be positive)
- `Interval` (string): Time interval for the data (default: '1m')

**Supported Intervals:**
- '1m', '3m', '5m', '15m', '30m', '45m', '1h', '2h', '3h', '4h', 'd', 'w', 'M'

**Example Response:**
```json
{
  "symbol": "BTCUSDT",
  "exchange": "BINANCE",
  "interval": "1h",
  "bars": 500,
  "data": [
    {
      "date": "2023-01-01T00:00:00",
      "open": 16500.50,
      "high": 16550.25,
      "low": 16480.75,
      "close": 16530.00,
      "volume": 1234.56
    },
    ...
  ]
}
```

## Configuration

The API runs on port 5000 by default. To change this, modify the port in `feederapi.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Change port as needed
```

## tvdatafeed Library

This project uses a custom fork of the tvdatafeed library by StreamAlpha that includes live data retrieving features. The library provides access to TradingView's historical market data without requiring a premium subscription.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to StreamAlpha for the original tvdatafeed library
- TradingView for providing financial market data