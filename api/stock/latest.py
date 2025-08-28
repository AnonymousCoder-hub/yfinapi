from http.server import BaseHTTPRequestHandler
import json
import yfinance as yf
from urllib.parse import parse_qs, urlparse
import pandas as pd

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            symbol = query_params.get('symbol', [''])[0]
            
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
            info = stock.info
            history = stock.history(period="1d")
            
            if history.empty:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": f"No data found for symbol: {symbol}"
                }).encode())
                return
            
            # Get latest data
            latest = history.iloc[-1]
            
            # Prepare response
            response_data = {
                "symbol": symbol,
                "company_name": info.get('longName', info.get('shortName', symbol)),
                "exchange": info.get('exchange', ''),
                "currency": info.get('currency', 'INR'),
                "latest_data": {
                    "date": latest.name.strftime('%Y-%m-%d'),
                    "open": round(float(latest['Open']), 2),
                    "high": round(float(latest['High']), 2),
                    "low": round(float(latest['Low']), 2),
                    "close": round(float(latest['Close']), 2),
                    "volume": int(latest['Volume']),
                    "change": round(float(latest['Close'] - latest['Open']), 2),
                    "change_percent": round(((float(latest['Close']) - float(latest['Open'])) / float(latest['Open'])) * 100, 2)
                },
                "company_info": {
                    "sector": info.get('sector', ''),
                    "industry": info.get('industry', ''),
                    "market_cap": info.get('marketCap', ''),
                    "pe_ratio": info.get('trailingPE', ''),
                    "dividend_yield": info.get('dividendYield', ''),
                    "52_week_high": info.get('fiftyTwoWeekHigh', ''),
                    "52_week_low": info.get('fiftyTwoWeekLow', ''),
                    "website": info.get('website', ''),
                    "business_summary": info.get('businessSummary', '')[:200] + '...' if info.get('businessSummary') and len(info.get('businessSummary', '')) > 200 else info.get('businessSummary', '')
                }
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