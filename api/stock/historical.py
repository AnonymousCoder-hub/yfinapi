from http.server import BaseHTTPRequestHandler
import json
import yfinance as yf
from urllib.parse import parse_qs, urlparse
import pandas as pd
from datetime import datetime, timedelta

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            symbol = query_params.get('symbol', [''])[0]
            start_date = query_params.get('start', [''])[0]
            end_date = query_params.get('end', [''])[0]
            period = query_params.get('period', ['1mo'])[0]
            interval = query_params.get('interval', ['1d'])[0]
            
            if not symbol:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Symbol parameter is required"
                }).encode())
                return
            
            # Fetch stock data
            stock = yf.Ticker(symbol)
            
            # Determine how to fetch data
            if start_date and end_date:
                history = stock.history(start=start_date, end=end_date, interval=interval)
            else:
                history = stock.history(period=period, interval=interval)
            
            if history.empty:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": f"No historical data found for symbol: {symbol}"
                }).encode())
                return
            
            # Convert to list of dictionaries
            historical_data = []
            for date, row in history.iterrows():
                historical_data.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "open": round(float(row['Open']), 2),
                    "high": round(float(row['High']), 2),
                    "low": round(float(row['Low']), 2),
                    "close": round(float(row['Close']), 2),
                    "volume": int(row['Volume']),
                    "change": round(float(row['Close'] - row['Open']), 2),
                    "change_percent": round(((float(row['Close']) - float(row['Open'])) / float(row['Open'])) * 100, 2)
                })
            
            # Calculate summary statistics
            closes = [item['close'] for item in historical_data]
            
            response_data = {
                "symbol": symbol,
                "period": period if not (start_date and end_date) else f"{start_date} to {end_date}",
                "interval": interval,
                "total_records": len(historical_data),
                "summary": {
                    "highest_price": max(closes),
                    "lowest_price": min(closes),
                    "average_price": round(sum(closes) / len(closes), 2),
                    "total_volume": sum([item['volume'] for item in historical_data]),
                    "price_change": round(closes[-1] - closes[0], 2),
                    "price_change_percent": round(((closes[-1] - closes[0]) / closes[0]) * 100, 2)
                },
                "data": historical_data
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())