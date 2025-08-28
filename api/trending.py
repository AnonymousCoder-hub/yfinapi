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
            
            exchange = query_params.get('exchange', ['nse'])[0].lower()
            limit = int(query_params.get('limit', [20])[0])
            
            # Popular Indian stocks by market cap and trading volume
            trending_stocks = {
                'nse': [
                    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
                    'ICICIBANK.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'ITC.NS', 'LT.NS',
                    'KOTAKBANK.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'SUNPHARMA.NS',
                    'TITAN.NS', 'ULTRACEMCO.NS', 'ONGC.NS', 'NESTLEIND.NS', 'WIPRO.NS',
                    'POWERGRID.NS', 'NTPC.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 'TECHM.NS'
                ],
                'bse': [
                    'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'INFY.BO', 'HINDUNILVR.BO',
                    'ICICIBANK.BO', 'BHARTIARTL.BO', 'SBIN.BO', 'ITC.BO', 'LT.BO',
                    'KOTAKBANK.BO', 'AXISBANK.BO', 'ASIANPAINT.BO', 'MARUTI.BO', 'SUNPHARMA.BO',
                    'TITAN.BO', 'ULTRACEMCO.BO', 'ONGC.BO', 'NESTLEIND.BO', 'WIPRO.BO'
                ]
            }
            
            stocks_to_check = trending_stocks.get(exchange, trending_stocks['nse'])[:limit]
            trending_data = []
            
            for symbol in stocks_to_check:
                try:
                    stock = yf.Ticker(symbol)
                    history = stock.history(period="5d")
                    info = stock.info
                    
                    if not history.empty:
                        latest = history.iloc[-1]
                        prev = history.iloc[-2] if len(history) > 1 else history.iloc[-1]
                        
                        trending_data.append({
                            "symbol": symbol,
                            "name": info.get('longName', info.get('shortName', symbol.replace('.NS', '').replace('.BO', ''))),
                            "current_price": round(float(latest['Close']), 2),
                            "change": round(float(latest['Close'] - prev['Close']), 2),
                            "change_percent": round(((float(latest['Close']) - float(prev['Close'])) / float(prev['Close'])) * 100, 2),
                            "volume": int(latest['Volume']),
                            "market_cap": info.get('marketCap', 0),
                            "sector": info.get('sector', ''),
                            "exchange": exchange.upper()
                        })
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {e}")
                    continue
            
            # Sort by volume (trending indicator)
            trending_data.sort(key=lambda x: x['volume'], reverse=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "exchange": exchange.upper(),
                "total_stocks": len(trending_data),
                "trending_stocks": trending_data
            }, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())