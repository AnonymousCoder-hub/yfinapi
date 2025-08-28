from http.server import BaseHTTPRequestHandler
import json
import yfinance as yf
import pandas as pd
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            query = query_params.get('q', [''])[0]
            exchange = query_params.get('exchange', ['both'])[0].lower()
            limit = int(query_params.get('limit', [50])[0])
            
            if not query:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Query parameter 'q' is required"
                }).encode())
                return
            
            # Indian stock symbols - most relevant companies
            indian_stocks = {
                'nse': [
                    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
                    'ICICIBANK.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'LICI.NS', 'ITC.NS',
                    'LT.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
                    'SUNPHARMA.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'ONGC.NS', 'NESTLEIND.NS',
                    'WIPRO.NS', 'POWERGRID.NS', 'NTPC.NS', 'BAJFINANCE.NS', 'HCLTECH.NS',
                    'TECHM.NS', 'M&M.NS', 'TATAMOTORS.NS', 'COALINDIA.NS', 'DIVISLAB.NS',
                    'BAJAJFINSV.NS', 'GRASIM.NS', 'ADANIPORTS.NS', 'JSWSTEEL.NS', 'HINDALCO.NS',
                    'TATASTEEL.NS', 'CIPLA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'APOLLOHOSP.NS',
                    'BRITANNIA.NS', 'BPCL.NS', 'UPL.NS', 'ADANIENT.NS', 'SBILIFE.NS',
                    'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'BAJAJ-AUTO.NS', 'SHREE.NS', 'TRENT.NS'
                ],
                'bse': [
                    'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'INFY.BO', 'HINDUNILVR.BO',
                    'ICICIBANK.BO', 'BHARTIARTL.BO', 'SBIN.BO', 'LICI.BO', 'ITC.BO',
                    'LT.BO', 'KOTAKBANK.BO', 'AXISBANK.BO', 'ASIANPAINT.BO', 'MARUTI.BO',
                    'SUNPHARMA.BO', 'TITAN.BO', 'ULTRACEMCO.BO', 'ONGC.BO', 'NESTLEIND.BO',
                    'WIPRO.BO', 'POWERGRID.BO', 'NTPC.BO', 'BAJFINANCE.BO', 'HCLTECH.BO',
                    'TECHM.BO', 'M&M.BO', 'TATAMOTORS.BO', 'COALINDIA.BO', 'DIVISLAB.BO'
                ]
            }
            
            results = []
            
            # Search logic
            if exchange in ['nse', 'both']:
                for symbol in indian_stocks['nse']:
                    company_name = symbol.replace('.NS', '')
                    if query.upper() in company_name or company_name in query.upper():
                        results.append({
                            'symbol': symbol,
                            'name': company_name,
                            'exchange': 'NSE',
                            'relevance_score': self.calculate_relevance(query, company_name)
                        })
            
            if exchange in ['bse', 'both']:
                for symbol in indian_stocks['bse']:
                    company_name = symbol.replace('.BO', '')
                    if query.upper() in company_name or company_name in query.upper():
                        # Skip if already added from NSE
                        if not any(r['name'] == company_name and r['exchange'] == 'NSE' for r in results):
                            results.append({
                                'symbol': symbol,
                                'name': company_name,
                                'exchange': 'BSE',
                                'relevance_score': self.calculate_relevance(query, company_name)
                            })
            
            # Sort by relevance score (higher is better)
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            results = results[:limit]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "query": query,
                "exchange": exchange,
                "total_results": len(results),
                "results": results
            }, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
    
    def calculate_relevance(self, query, company_name):
        """Calculate relevance score for search results"""
        query = query.upper()
        company = company_name.upper()
        
        # Exact match gets highest score
        if query == company:
            return 100
        # Starts with query
        elif company.startswith(query):
            return 80
        # Contains query
        elif query in company:
            return 60
        # Partial match
        else:
            return 20