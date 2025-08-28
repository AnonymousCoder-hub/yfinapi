# 🇮🇳 Indian Stocks Data API

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyourusername%2Findian-stocks-api&project-name=indian-stocks-api&repository-name=indian-stocks-api)

A comprehensive **Indian Stock Market Data API** built with Python, yfinance, and deployable on Vercel. Get real-time and historical data for NSE & BSE stocks, market indices, trending stocks, gainers/losers, and much more!

## 🚀 Features

- **Real-time Stock Data** - Latest prices, volume, market cap
- **Historical Data** - Custom date ranges and intervals
- **Market Indices** - NIFTY 50, SENSEX, sectoral indices
- **Trending Stocks** - Most active by volume
- **Gainers & Losers** - Top performing stocks
- **Sector Analysis** - Performance by industry sectors
- **Market Status** - Live market hours and status
- **Fundamentals** - Complete company financials and ratios
- **Stock Search** - Intelligent symbol search with relevance scoring
- **Multi-Exchange** - Support for NSE (.NS) and BSE (.BO)

## 🏗️ Architecture

- **Backend**: Python with yfinance library
- **Deployment**: Vercel Serverless Functions
- **Data Source**: Yahoo Finance
- **Format**: Pure JSON responses
- **CORS**: Enabled for browser access

## 📋 API Endpoints

### Base URL: `https://your-app-name.vercel.app/api`

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `/` | API Documentation | - |
| `/search` | Search stock symbols | `q`, `exchange`, `limit` |
| `/stock/latest` | Latest stock data | `symbol` |
| `/stock/historical` | Historical data | `symbol`, `start`, `end`, `period`, `interval` |
| `/trending` | Trending stocks | `exchange`, `limit` |
| `/gainers` | Top gainers | `exchange`, `limit` |
| `/losers` | Top losers | `exchange`, `limit` |
| `/indices` | Market indices | `period` |
| `/market-status` | Market status | - |
| `/sectors` | Sector analysis | `exchange` |
| `/fundamentals` | Company fundamentals | `symbol` |

## 🔗 Example Usage

### Search for stocks
```
GET /api/search?q=reliance&exchange=nse&limit=10
```

### Get latest stock data
```
GET /api/stock/latest?symbol=RELIANCE.NS
```

### Historical data with custom range
```
GET /api/stock/historical?symbol=TCS.NS&start=2024-01-01&end=2024-12-31&interval=1d
```

### Top 15 gainers on NSE
```
GET /api/gainers?exchange=nse&limit=15
```

### Market indices
```
GET /api/indices?period=1d
```

### Current market status
```
GET /api/market-status
```

## 🚀 Quick Deploy to Vercel

### Method 1: One-Click Deploy (Recommended)

1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account
3. Clone this repository to your GitHub
4. Vercel will automatically deploy your API
5. Your API will be live at `https://your-project-name.vercel.app/api`

### Method 2: Manual Deploy

1. **Fork this repository** to your GitHub account

2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/indian-stocks-api.git
   cd indian-stocks-api
   ```

3. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

4. **Deploy to Vercel**:
   ```bash
   vercel
   ```

5. **Follow the prompts**:
   - Link to existing project? `N`
   - Project name: `indian-stocks-api` (or your preferred name)
   - Directory: `./` (current directory)
   - Want to override settings? `N`

6. **Your API is live!** 🎉

## 📁 Project Structure

```
indian-stocks-api/
├── api/                          # Vercel API routes
│   ├── index.py                  # API documentation endpoint
│   ├── search.py                 # Stock symbol search
│   ├── stock/
│   │   ├── latest.py            # Latest stock data
│   │   └── historical.py        # Historical data
│   ├── trending.py               # Trending stocks
│   ├── gainers.py               # Top gainers
│   ├── losers.py                # Top losers
│   ├── indices.py               # Market indices
│   ├── market-status.py         # Market status
│   ├── sectors.py               # Sector analysis
│   └── fundamentals.py          # Company fundamentals
├── vercel.json                   # Vercel configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🛠️ Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/indian-stocks-api.git
   cd indian-stocks-api
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

4. **Run locally**:
   ```bash
   vercel dev
   ```

5. **Access your API**: `http://localhost:3000/api`

## 📊 Sample Response

### Latest Stock Data (`/api/stock/latest?symbol=RELIANCE.NS`)

```json
{
  "symbol": "RELIANCE.NS",
  "company_name": "Reliance Industries Limited",
  "exchange": "NSI",
  "currency": "INR",
  "latest_data": {
    "date": "2024-08-20",
    "open": 2756.50,
    "high": 2789.95,
    "low": 2751.00,
    "close": 2782.40,
    "volume": 8547293,
    "change": 25.90,
    "change_percent": 0.94
  },
  "company_info": {
    "sector": "Energy",
    "industry": "Oil & Gas Refining & Marketing",
    "market_cap": 18742175744000,
    "pe_ratio": 26.84,
    "dividend_yield": 0.0033,
    "52_week_high": 3024.90,
    "52_week_low": 2220.30,
    "website": "http://www.ril.com"
  }
}
```

## 🎯 Common Stock Symbols

### NSE Format (.NS)
- `RELIANCE.NS` - Reliance Industries
- `TCS.NS` - Tata Consultancy Services
- `HDFCBANK.NS` - HDFC Bank
- `INFY.NS` - Infosys
- `ICICIBANK.NS` - ICICI Bank

### BSE Format (.BO)
- `RELIANCE.BO` - Reliance Industries
- `TCS.BO` - Tata Consultancy Services
- `HDFCBANK.BO` - HDFC Bank
- `INFY.BO` - Infosys
- `ICICIBANK.BO` - ICICI Bank

## 🕐 Market Hours

- **Trading Hours**: 9:15 AM - 3:30 PM IST
- **Days**: Monday to Friday
- **Timezone**: Asia/Kolkata (IST)

## ⚡ Rate Limits

This API uses Yahoo Finance data through yfinance. While there are no explicit rate limits set by this API, Yahoo Finance may throttle requests if you make too many concurrent calls. For production use, consider:

- Implementing caching
- Adding request queuing
- Using multiple data sources

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for providing easy access to Yahoo Finance data
- [Vercel](https://vercel.com) for serverless deployment platform
- Yahoo Finance for the underlying market data

## 📞 Support

If you encounter any issues or have questions:

1. Check the [API Documentation](https://your-app-name.vercel.app/api) endpoint
2. Open an issue on GitHub
3. Check Yahoo Finance data availability for specific symbols

## 🔮 Roadmap

- [ ] WebSocket support for real-time data
- [ ] Additional Indian exchanges (MCX, etc.)
- [ ] Options and derivatives data
- [ ] Technical indicators
- [ ] News sentiment analysis
- [ ] Portfolio tracking features

---

**Made with ❤️ for the Indian Stock Market**

Deploy your own instance in under 2 minutes! 👆 Click the deploy button above.
