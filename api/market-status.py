from http.server import BaseHTTPRequestHandler
import json
import yfinance as yf
from urllib.parse import parse_qs, urlparse
from datetime import datetime, time
import pytz

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Indian market timezone
            ist = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(ist)
            
            # NSE/BSE market hours (IST)
            market_open = time(9, 15)  # 9:15 AM
            market_close = time(15, 30)  # 3:30 PM
            
            current_time_only = current_time.time()
            is_weekend = current_time.weekday() >= 5  # Saturday = 5, Sunday = 6
            
            # Determine market status
            if is_weekend:
                market_status = "CLOSED"
                status_reason = "Weekend"
            elif market_open <= current_time_only <= market_close:
                market_status = "OPEN"
                status_reason = "Regular trading hours"
            else:
                market_status = "CLOSED"
                status_reason = "Outside trading hours"
            
            # Get NIFTY 50 for market snapshot
            try:
                nifty = yf.Ticker('^NSEI')
                nifty_history = nifty.history(period="1d")
                
                if not nifty_history.empty:
                    nifty_latest = nifty_history.iloc[-1]
                    nifty_data = {
                        "current_value": round(float(nifty_latest['Close']), 2),
                        "day_high": round(float(nifty_latest['High']), 2),
                        "day_low": round(float(nifty_latest['Low']), 2),
                        "volume": int(nifty_latest['Volume'])
                    }
                else:
                    nifty_data = None
            except:
                nifty_data = None
            
            # Get SENSEX for market snapshot
            try:
                sensex = yf.Ticker('^BSESN')
                sensex_history = sensex.history(period="1d")
                
                if not sensex_history.empty:
                    sensex_latest = sensex_history.iloc[-1]
                    sensex_data = {
                        "current_value": round(float(sensex_latest['Close']), 2),
                        "day_high": round(float(sensex_latest['High']), 2),
                        "day_low": round(float(sensex_latest['Low']), 2),
                        "volume": int(sensex_latest['Volume'])
                    }
                else:
                    sensex_data = None
            except:
                sensex_data = None
            
            response_data = {
                "current_time": current_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                "market_status": market_status,
                "status_reason": status_reason,
                "trading_hours": {
                    "open": "09:15 IST",
                    "close": "15:30 IST",
                    "timezone": "Asia/Kolkata"
                },
                "exchanges": {
                    "NSE": {
                        "status": market_status,
                        "name": "National Stock Exchange",
                        "currency": "INR"
                    },
                    "BSE": {
                        "status": market_status,
                        "name": "Bombay Stock Exchange",
                        "currency": "INR"
                    }
                },
                "market_snapshot": {
                    "nifty_50": nifty_data,
                    "sensex": sensex_data
                },
                "next_trading_session": {
                    "date": self.get_next_trading_day(current_time),
                    "opens_at": "09:15 IST"
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
    
    def get_next_trading_day(self, current_time):
        """Get next trading day (skip weekends)"""
        from datetime import timedelta
        
        next_day = current_time + timedelta(days=1)
        while next_day.weekday() >= 5:  # Skip weekends
            next_day += timedelta(days=1)
        
        return next_day.strftime('%Y-%m-%d')