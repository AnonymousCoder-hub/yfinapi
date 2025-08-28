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
            
            # Sector-wise Indian stocks
            sectors = {
                'Banking & Financial Services': {
                    'nse': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'SBILIFE.NS', 'HDFCLIFE.NS'],
                    'bse': ['HDFCBANK.BO', 'ICICIBANK.BO', 'SBIN.BO', 'KOTAKBANK.BO', 'AXISBANK.BO', 'BAJFINANCE.BO', 'BAJAJFINSV.BO']
                },
                'Information Technology': {
                    'nse': ['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HCLTECH.NS', 'TECHM.NS', 'LTI.NS', 'MINDTREE.NS'],
                    'bse': ['TCS.BO', 'INFY.BO', 'WIPRO.BO', 'HCLTECH.BO', 'TECHM.BO']
                },
                'Oil & Gas': {
                    'nse': ['RELIANCE.NS', 'ONGC.NS', 'BPCL.NS', 'IOC.NS', 'HINDPETRO.NS', 'GAIL.NS'],
                    'bse': ['RELIANCE.BO', 'ONGC.BO', 'BPCL.BO', 'IOC.BO']
                },
                'Automobiles': {
                    'nse': ['MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS', 'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 'EICHERMOT.NS', 'ASHOKLEY.NS'],
                    'bse': ['MARUTI.BO', 'TATAMOTORS.BO', 'M&M.BO', 'BAJAJ-AUTO.BO', 'HEROMOTOCO.BO']
                },
                'Pharmaceuticals': {
                    'nse': ['SUNPHARMA.NS', 'DIVISLAB.NS', 'CIPLA.NS', 'DRREDDY.NS', 'BIOCON.NS', 'LUPIN.NS'],
                    'bse': ['SUNPHARMA.BO', 'DIVISLAB.BO', 'CIPLA.BO', 'DRREDDY.BO']
                },
                'FMCG': {
                    'nse': ['HINDUNILVR.NS', 'ITC.NS', 'NESTLEIND.NS', 'BRITANNIA.NS', 'DABUR.NS', 'MARICO.NS'],
                    'bse': ['HINDUNILVR.BO', 'ITC.BO', 'NESTLEIND.BO', 'BRITANNIA.BO']
                },
                'Metals & Mining': {
                    'nse': ['TATASTEEL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'COALINDIA.NS', 'VEDL.NS', 'SAIL.NS'],
                    'bse': ['TATASTEEL.BO', 'JSWSTEEL.BO', 'HINDALCO.BO', 'COALINDIA.BO']
                },
                'Cement': {
                    'nse': ['ULTRACEMCO.NS', 'SHREECEM.NS', 'GRASIM.NS', 'AMBUJACEM.NS', 'ACC.NS'],
                    'bse': ['ULTRACEMCO.BO', 'SHREECEM.BO', 'GRASIM.BO', 'AMBUJACEM.BO']
                },
                'Textiles': {
                    'nse': ['WELSPUNIND.NS', 'ARVIND.NS', 'PAGEIND.NS', 'VIPIND.NS'],
                    'bse': ['WELSPUNIND.BO', 'ARVIND.BO']
                },
                'Telecommunications': {
                    'nse': ['BHARTIARTL.NS', 'IDEA.NS'],
                    'bse': ['BHARTIARTL.BO', 'IDEA.BO']
                }
            }
            
            sectors_data = {}
            
            for sector_name, sector_stocks in sectors.items():
                stocks_list = sector_stocks.get(exchange, sector_stocks.get('nse', []))
                sector_info = {
                    "sector_name": sector_name,
                    "total_stocks": len(stocks_list),
                    "stocks": [],
                    "sector_performance": {
                        "total_gainers": 0,
                        "total_losers": 0,
                        "average_change": 0
                    }
                }
                
                total_change = 0
                valid_stocks = 0
                
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
                            
                            stock_data = {
                                "symbol": symbol,
                                "name": info.get('longName', info.get('shortName', symbol.replace('.NS', '').replace('.BO', ''))),
                                "current_price": round(float(latest['Close']), 2),
                                "change": round(change, 2),
                                "change_percent": round(change_percent, 2),
                                "volume": int(latest['Volume']),
                                "market_cap": info.get('marketCap', 0)
                            }
                            
                            sector_info["stocks"].append(stock_data)
                            
                            # Update sector performance
                            if change > 0:
                                sector_info["sector_performance"]["total_gainers"] += 1
                            elif change < 0:
                                sector_info["sector_performance"]["total_losers"] += 1
                            
                            total_change += change_percent
                            valid_stocks += 1
                            
                    except Exception as e:
                        print(f"Error fetching data for {symbol}: {e}")
                        continue
                
                # Calculate average change for sector
                if valid_stocks > 0:
                    sector_info["sector_performance"]["average_change"] = round(total_change / valid_stocks, 2)
                
                # Sort stocks by change percentage
                sector_info["stocks"].sort(key=lambda x: x['change_percent'], reverse=True)
                
                sectors_data[sector_name] = sector_info
            
            # Sort sectors by average performance
            sorted_sectors = dict(sorted(sectors_data.items(), 
                                       key=lambda x: x[1]["sector_performance"]["average_change"], 
                                       reverse=True))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "exchange": exchange.upper(),
                "total_sectors": len(sorted_sectors),
                "sectors": sorted_sectors
            }, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())