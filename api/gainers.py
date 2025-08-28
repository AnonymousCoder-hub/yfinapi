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
            
            # Top Indian stocks to check for gainers
            stocks_to_check = {
                'nse': [
                    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
                    'ICICIBANK.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'ITC.NS', 'LT.NS',
                    'KOTAKBANK.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'SUNPHARMA.NS',
                    'TITAN.NS', 'ULTRACEMCO.NS', 'ONGC.NS', 'NESTLEIND.NS', 'WIPRO.NS',
                    'POWERGRID.NS', 'NTPC.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 'TECHM.NS',
                    'M&M.NS', 'TATAMOTORS.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'BAJAJFINSV.NS',
                    'GRASIM.NS', 'ADANIPORTS.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'TATASTEEL.NS',
                    'CIPLA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'APOLLOHOSP.NS', 'BRITANNIA.NS'
                ],
                'bse': [
                    'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'INFY.BO', 'HINDUNILVR.BO',
                    'ICICIBANK.BO', 'BHARTIARTL.BO', 'SBIN.BO', 'ITC.BO', 'LT.BO',
                    'KOTAKBANK.BO', 'AXISBANK.BO', 'ASIANPAINT.BO', 'MARUTI.BO', 'SUNPHARMA.BO',
                    'TITAN.BO', 'ULTRACEMCO.BO', 'ONGC.BO', 'NESTLEIND.BO', 'WIPRO.BO',
                    'POWERGRID.BO', 'NTPC.BO', 'BAJFINANCE.BO', 'HCLTECH.BO', 'TECHM.BO'
                ]
            }
            
            stocks_list = stocks_to_check.get(exchange, stocks_to_check['nse'])
            gainers_data = []
            
            for symbol in stocks_list:
                try:
                    stock = yf.Ticker(symbol)
                    history = stock.history(period="2d")
                    info = stock.info
                    
                    if len(history) >= 2:
                        latest = history.iloc[-1]
                        previous = history.iloc[-2]
                        
                        change = float(latest['Close'] - previous['Close'])
                        change_percent = ((float(latest['Close']) - float(previous['Close'])) / float(previous['Close'])) * 100
                        
                        if change > 0:  # Only gainers
                            gainers_data.append({
                                "symbol": symbol,
                                "name": info.get('longName', info.get('shortName', symbol.replace('.NS', '').replace('.BO', ''))),
                                "current_price": round(float(latest['Close']), 2),
                                "previous_close": round(float(previous['Close']), 2),
                                "change": round(change, 2),
                                "change_percent": round(change_percent, 2),
                                "volume": int(latest['Volume']),
                                "high": round(float(latest['High']), 2),
                                "low": round(float(latest['Low']), 2),
                                "market_cap": info.get('marketCap', 0),
                                "sector": info.get('sector', ''),
                                "exchange": exchange.upper()
                            })
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {e}")
                    continue
            
            # Sort by change percentage (highest gainers first)
            gainers_data.sort(key=lambda x: x['change_percent'], reverse=True)
            gainers_data = gainers_data[:limit]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "exchange": exchange.upper(),
                "date": history.index[-1].strftime('%Y-%m-%d') if not history.empty else None,
                "total_gainers": len(gainers_data),
                "top_gainers": gainers_data
            }, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())