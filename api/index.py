from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # API Documentation
            api_docs = {
                "api_name": "Indian Stocks Data API",
                "version": "1.0.0",
                "description": "Comprehensive Indian stock market data API using yfinance",
                "base_url": "https://your-vercel-app.vercel.app/api",
                "endpoints": {
                    "search": {
                        "url": "/api/search",
                        "method": "GET",
                        "description": "Search for Indian stock symbols",
                        "parameters": {
                            "q": "Search query (required)",
                            "exchange": "nse|bse|both (default: both)",
                            "limit": "Number of results (default: 50)"
                        },
                        "example": "/api/search?q=reliance&exchange=nse&limit=10"
                    },
                    "latest_stock_data": {
                        "url": "/api/stock/latest",
                        "method": "GET",
                        "description": "Get latest data for a specific stock",
                        "parameters": {
                            "symbol": "Stock symbol (required) - e.g., RELIANCE.NS"
                        },
                        "example": "/api/stock/latest?symbol=RELIANCE.NS"
                    },
                    "historical_data": {
                        "url": "/api/stock/historical",
                        "method": "GET",
                        "description": "Get historical stock data with custom date range",
                        "parameters": {
                            "symbol": "Stock symbol (required)",
                            "start": "Start date (YYYY-MM-DD) - optional",
                            "end": "End date (YYYY-MM-DD) - optional",
                            "period": "1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max (default: 1mo)",
                            "interval": "1m|2m|5m|15m|30m|60m|90m|1h|1d|5d|1wk|1mo|3mo (default: 1d)"
                        },
                        "example": "/api/stock/historical?symbol=TCS.NS&period=6mo&interval=1d"
                    },
                    "trending_stocks": {
                        "url": "/api/trending",
                        "method": "GET",
                        "description": "Get trending stocks by trading volume",
                        "parameters": {
                            "exchange": "nse|bse (default: nse)",
                            "limit": "Number of results (default: 20)"
                        },
                        "example": "/api/trending?exchange=nse&limit=15"
                    },
                    "top_gainers": {
                        "url": "/api/gainers",
                        "method": "GET",
                        "description": "Get top gaining stocks",
                        "parameters": {
                            "exchange": "nse|bse (default: nse)",
                            "limit": "Number of results (default: 20)"
                        },
                        "example": "/api/gainers?exchange=bse&limit=10"
                    },
                    "top_losers": {
                        "url": "/api/losers",
                        "method": "GET",
                        "description": "Get top losing stocks",
                        "parameters": {
                            "exchange": "nse|bse (default: nse)",
                            "limit": "Number of results (default: 20)"
                        },
                        "example": "/api/losers?exchange=nse&limit=15"
                    },
                    "market_indices": {
                        "url": "/api/indices",
                        "method": "GET",
                        "description": "Get major Indian market indices (NIFTY, SENSEX, etc.)",
                        "parameters": {
                            "period": "1d|5d|1mo|3mo|6mo|1y (default: 1d)"
                        },
                        "example": "/api/indices?period=1d"
                    },
                    "market_status": {
                        "url": "/api/market-status",
                        "method": "GET",
                        "description": "Get current market status and trading hours",
                        "parameters": "None",
                        "example": "/api/market-status"
                    },
                    "sectors": {
                        "url": "/api/sectors",
                        "method": "GET",
                        "description": "Get sector-wise stock performance",
                        "parameters": {
                            "exchange": "nse|bse (default: nse)"
                        },
                        "example": "/api/sectors?exchange=nse"
                    },
                    "fundamentals": {
                        "url": "/api/fundamentals",
                        "method": "GET",
                        "description": "Get comprehensive fundamental data for a stock",
                        "parameters": {
                            "symbol": "Stock symbol (required) - e.g., HDFCBANK.NS"
                        },
                        "example": "/api/fundamentals?symbol=HDFCBANK.NS"
                    }
                },
                "common_stock_symbols": {
                    "NSE_format": [
                        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
                        "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "ITC.NS", "LT.NS"
                    ],
                    "BSE_format": [
                        "RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "HINDUNILVR.BO",
                        "ICICIBANK.BO", "BHARTIARTL.BO", "SBIN.BO", "ITC.BO", "LT.BO"
                    ]
                },
                "market_indices_symbols": {
                    "NIFTY_50": "^NSEI",
                    "SENSEX": "^BSESN",
                    "NIFTY_BANK": "^NSEBANK",
                    "NIFTY_IT": "^CNXIT",
                    "NIFTY_AUTO": "^CNXAUTO"
                },
                "usage_notes": [
                    "All prices are in INR (Indian Rupees)",
                    "Data is sourced from Yahoo Finance via yfinance library",
                    "Market hours: 9:15 AM to 3:30 PM IST (Monday to Friday)",
                    "NSE symbols end with .NS, BSE symbols end with .BO",
                    "Historical data may have limitations based on yfinance availability",
                    "Rate limiting may apply for excessive requests"
                ],
                "error_handling": {
                    "400": "Bad Request - Missing required parameters",
                    "404": "Not Found - Symbol not found or no data available",
                    "500": "Internal Server Error - API processing error"
                }
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(api_docs, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())