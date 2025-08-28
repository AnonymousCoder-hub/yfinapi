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
            
            # Get financial data
            try:
                financials = stock.financials
                balance_sheet = stock.balance_sheet
                cashflow = stock.cashflow
            except:
                financials = None
                balance_sheet = None
                cashflow = None
            
            # Prepare fundamentals data
            fundamentals = {
                "symbol": symbol,
                "company_info": {
                    "name": info.get('longName', info.get('shortName', '')),
                    "sector": info.get('sector', ''),
                    "industry": info.get('industry', ''),
                    "country": info.get('country', ''),
                    "website": info.get('website', ''),
                    "business_summary": info.get('businessSummary', ''),
                    "full_time_employees": info.get('fullTimeEmployees', 0)
                },
                "market_data": {
                    "market_cap": info.get('marketCap', 0),
                    "enterprise_value": info.get('enterpriseValue', 0),
                    "shares_outstanding": info.get('sharesOutstanding', 0),
                    "float_shares": info.get('floatShares', 0),
                    "currency": info.get('currency', 'INR')
                },
                "valuation_metrics": {
                    "pe_ratio": info.get('trailingPE', 0),
                    "forward_pe": info.get('forwardPE', 0),
                    "peg_ratio": info.get('pegRatio', 0),
                    "price_to_book": info.get('priceToBook', 0),
                    "price_to_sales": info.get('priceToSalesTrailing12Months', 0),
                    "enterprise_to_revenue": info.get('enterpriseToRevenue', 0),
                    "enterprise_to_ebitda": info.get('enterpriseToEbitda', 0)
                },
                "financial_metrics": {
                    "revenue": info.get('totalRevenue', 0),
                    "revenue_growth": info.get('revenueGrowth', 0),
                    "gross_profit": info.get('grossProfits', 0),
                    "operating_margins": info.get('operatingMargins', 0),
                    "profit_margins": info.get('profitMargins', 0),
                    "return_on_assets": info.get('returnOnAssets', 0),
                    "return_on_equity": info.get('returnOnEquity', 0),
                    "debt_to_equity": info.get('debtToEquity', 0),
                    "current_ratio": info.get('currentRatio', 0),
                    "quick_ratio": info.get('quickRatio', 0)
                },
                "dividend_info": {
                    "dividend_rate": info.get('dividendRate', 0),
                    "dividend_yield": info.get('dividendYield', 0),
                    "payout_ratio": info.get('payoutRatio', 0),
                    "ex_dividend_date": info.get('exDividendDate', ''),
                    "dividend_date": info.get('dividendDate', '')
                },
                "price_data": {
                    "current_price": info.get('currentPrice', 0),
                    "previous_close": info.get('previousClose', 0),
                    "day_high": info.get('dayHigh', 0),
                    "day_low": info.get('dayLow', 0),
                    "52_week_high": info.get('fiftyTwoWeekHigh', 0),
                    "52_week_low": info.get('fiftyTwoWeekLow', 0),
                    "50_day_average": info.get('fiftyDayAverage', 0),
                    "200_day_average": info.get('twoHundredDayAverage', 0)
                },
                "trading_info": {
                    "volume": info.get('volume', 0),
                    "average_volume": info.get('averageVolume', 0),
                    "average_volume_10days": info.get('averageVolume10days', 0),
                    "bid": info.get('bid', 0),
                    "ask": info.get('ask', 0),
                    "bid_size": info.get('bidSize', 0),
                    "ask_size": info.get('askSize', 0)
                },
                "analyst_info": {
                    "target_high_price": info.get('targetHighPrice', 0),
                    "target_low_price": info.get('targetLowPrice', 0),
                    "target_mean_price": info.get('targetMeanPrice', 0),
                    "target_median_price": info.get('targetMedianPrice', 0),
                    "recommendation_mean": info.get('recommendationMean', 0),
                    "recommendation_key": info.get('recommendationKey', ''),
                    "number_of_analyst_opinions": info.get('numberOfAnalystOpinions', 0)
                }
            }
            
            # Add financial statements summary if available
            if financials is not None and not financials.empty:
                try:
                    latest_financials = financials.iloc[:, 0].to_dict()
                    fundamentals["recent_financials"] = {
                        "total_revenue": float(latest_financials.get('Total Revenue', 0)) if pd.notna(latest_financials.get('Total Revenue', 0)) else 0,
                        "gross_profit": float(latest_financials.get('Gross Profit', 0)) if pd.notna(latest_financials.get('Gross Profit', 0)) else 0,
                        "operating_income": float(latest_financials.get('Operating Income', 0)) if pd.notna(latest_financials.get('Operating Income', 0)) else 0,
                        "net_income": float(latest_financials.get('Net Income', 0)) if pd.notna(latest_financials.get('Net Income', 0)) else 0
                    }
                except:
                    fundamentals["recent_financials"] = None
            else:
                fundamentals["recent_financials"] = None
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(fundamentals, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())