# 🚀 Deployment Guide - Indian Stocks API

## Quick Start (2 minutes)

### Option 1: One-Click Deploy with Vercel Button

1. **Click the Deploy Button** in the README.md
2. **Connect GitHub** - Authorize Vercel to access your GitHub
3. **Clone Repository** - Vercel will fork this repo to your GitHub account
4. **Automatic Deployment** - Vercel deploys your API automatically
5. **API Ready!** - Access at `https://your-project-name.vercel.app/api`

### Option 2: Manual GitHub + Vercel Deploy

1. **Fork this Repository**
   - Go to GitHub and fork this repository
   - Clone your fork: `git clone https://github.com/YOUR_USERNAME/indian-stocks-api.git`

2. **Deploy to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Connect your GitHub account
   - Import your forked repository
   - Vercel auto-detects the configuration
   - Deploy!

## 📁 File Structure Overview

```
indian-stocks-api/
├── 📄 vercel.json              # Vercel deployment config
├── 📄 requirements.txt         # Python dependencies
├── 📄 package.json            # NPM config (for Vercel CLI)
├── 📄 README.md               # Main documentation
├── 📄 DEPLOYMENT_GUIDE.md     # This file
├── 📄 LICENSE                 # MIT License
├── 📄 .gitignore             # Git ignore rules
├── 📄 test_api.py            # Local testing script
└── 📁 api/                   # Vercel API endpoints
    ├── 📄 index.py           # API docs & main endpoint
    ├── 📄 search.py          # Stock symbol search
    ├── 📄 trending.py        # Trending stocks
    ├── 📄 gainers.py         # Top gainers
    ├── 📄 losers.py          # Top losers  
    ├── 📄 indices.py         # Market indices
    ├── 📄 market-status.py   # Market status
    ├── 📄 sectors.py         # Sector analysis
    ├── 📄 fundamentals.py    # Company fundamentals
    └── 📁 stock/
        ├── 📄 latest.py      # Latest stock data
        └── 📄 historical.py  # Historical data
```

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- Node.js 16+ (for Vercel CLI)
- Git

### Setup Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/indian-stocks-api.git
   cd indian-stocks-api
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   # OR
   yarn global add vercel
   ```

4. **Run Locally**
   ```bash
   vercel dev
   ```

5. **Test API**
   - API docs: `http://localhost:3000/api`
   - Test script: `python test_api.py`

### Local Testing Commands

```bash
# Test all endpoints
python test_api.py

# Test specific endpoint with curl
curl "http://localhost:3000/api/search?q=reliance&limit=5"
curl "http://localhost:3000/api/stock/latest?symbol=TCS.NS"
curl "http://localhost:3000/api/gainers?exchange=nse&limit=10"
```

## 🌐 Production Deployment

### Vercel Configuration

The `vercel.json` file configures Python runtime:

```json
{
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    }
  ]
}
```

### Environment Variables (Optional)

While not required for basic functionality, you can set these in Vercel dashboard:

- `PYTHON_VERSION`: `3.9` (default)
- `YF_TIMEOUT`: `30` (yfinance timeout in seconds)

### Custom Domain Setup

1. **In Vercel Dashboard**:
   - Go to Project Settings
   - Click "Domains"
   - Add your custom domain
   - Configure DNS records as shown

2. **Update README**:
   - Replace `your-app-name.vercel.app` with your custom domain
   - Update the deploy button URL

## 🔧 Configuration Options

### Modifying Stock Lists

Edit the stock arrays in each endpoint file:

```python
# In api/search.py, api/gainers.py, etc.
indian_stocks = {
    'nse': [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS',
        # Add more NSE stocks here
    ],
    'bse': [
        'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO',
        # Add more BSE stocks here  
    ]
}
```

### Adding New Endpoints

1. **Create new file** in `/api/` directory
2. **Use this template**:

```python
from http.server import BaseHTTPRequestHandler
import json
import yfinance as yf
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Your logic here
            response_data = {"message": "Hello World"}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
```

## 🐛 Troubleshooting

### Common Issues

1. **"No module named yfinance"**
   - Ensure `requirements.txt` is in the root directory
   - Verify yfinance version: `yfinance==0.2.28`

2. **Timeout errors**
   - Yahoo Finance may be slow, increase timeout
   - Some stocks may not have data available

3. **CORS errors**
   - Headers are already configured for cross-origin requests
   - Check browser console for specific errors

4. **Deploy button not working**
   - Ensure the GitHub URL in README is correct
   - Repository must be public for the deploy button

### Performance Optimization

1. **Add caching** (Redis/Memcached)
2. **Batch API calls** for multiple stocks
3. **Use async/await** for concurrent requests
4. **Implement rate limiting**

### Monitoring

- **Vercel Analytics**: Built-in performance monitoring
- **Function Logs**: View in Vercel dashboard
- **Error Tracking**: Add Sentry or similar service

## 🔒 Security Considerations

1. **Rate Limiting**: Implement if needed
2. **API Keys**: No external API keys required for basic functionality
3. **Input Validation**: Already implemented for parameters
4. **HTTPS**: Automatically enforced by Vercel

## 📈 Scaling

### Serverless Benefits
- **Auto-scaling**: Handles traffic spikes automatically
- **Cost-effective**: Pay only for requests
- **Global CDN**: Fast worldwide access

### Upgrade Options
- **Vercel Pro**: Higher limits, better performance
- **Database**: Add MongoDB/PostgreSQL for caching
- **Queue System**: For heavy processing tasks

## 🎯 Next Steps

After deployment, consider:

1. **Custom Domain**: Professional appearance
2. **API Documentation**: Interactive docs with Swagger
3. **Client Libraries**: SDKs for popular languages
4. **Webhooks**: Real-time data notifications
5. **Authentication**: JWT-based auth for premium features

## 📞 Getting Help

- **GitHub Issues**: Report bugs or request features
- **Vercel Support**: Deployment and infrastructure questions
- **yfinance Docs**: Data source questions
- **Community**: Stack Overflow with tags: `yfinance`, `vercel`, `indian-stocks`

---

🎉 **You're now ready to deploy your Indian Stocks API!**

Click the deploy button in the main README or follow the manual steps above.