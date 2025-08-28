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
            
            period = query_params.get('period', ['1d'])[0]
            
            # Major Indian market indices
            indices = {
                'NIFTY 50': '^NSEI',
                'SENSEX': '^BSESN',
                'NIFTY BANK': '^NSEBANK',
                'NIFTY IT': '^CNXIT',
                'NIFTY AUTO': '^CNXAUTO',
                'NIFTY PHARMA': '^CNXPHARMA',
                'NIFTY FMCG': '^CNXFMCG',
                'NIFTY METAL': '^CNXMETAL',
                'NIFTY REALTY': '^CNXREALTY',
                'NIFTY ENERGY': '^CNXENERGY',
                'NIFTY NEXT 50': '^NSMIDCP',
                'NIFTY MIDCAP 100': '^NSEMDCP50'
            }
            
            indices_data = []
            
            for index_name, symbol in indices.items():
                try:
                    index_ticker = yf.Ticker(symbol)
                    history = index_ticker.history(period=period)
                    info = index_ticker.info
                    
                    if not history.empty:
                        latest = history.iloc[-1]
                        previous = history.iloc[-2] if len(history) > 1 else history.iloc[0]
                        
                        change = float(latest['Close'] - previous['Close'])
                        change_percent = ((float(latest['Close']) - float(previous['Close'])) / float(previous['Close'])) * 100
                        
                        indices_data.append({
                            "name": index_name,
                            "symbol": symbol,
                            "current_value": round(float(latest['Close']), 2),
                            "previous_close": round(float(previous['Close']), 2),
                            "change": round(change, 2),
                            "change_percent": round(change_percent, 2),
                            "day_high": round(float(latest['High']), 2),
                            "day_low": round(float(latest['Low']), 2),
                            "volume": int(latest['Volume']) if latest['Volume'] > 0 else 0,
                            "date": latest.name.strftime('%Y-%m-%d'),
                            "52_week_high": round(float(max(history['High'])), 2),
                            "52_week_low": round(float(min(history['Low'])), 2)
                        })
                except Exception as e:
                    print(f"Error fetching data for {index_name}: {e}")
                    continue
            
            # Sort by change percentage
            indices_data.sort(key=lambda x: x['change_percent'], reverse=True)
            
            # Market summary
            total_gainers = len([idx for idx in indices_data if idx['change'] > 0])
            total_losers = len([idx for idx in indices_data if idx['change'] < 0])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "period": period,
                "total_indices": len(indices_data),
                "market_summary": {
                    "total_gainers": total_gainers,
                    "total_losers": total_losers,
                    "unchanged": len(indices_data) - total_gainers - total_losers
                },
                "indices": indices_data
            }, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())