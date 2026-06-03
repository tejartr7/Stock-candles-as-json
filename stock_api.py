import yfinance as yf
from config import INDIAN_STOCK_SUFFIX
import requests

class StockAPI:
    @staticmethod
    def search_symbols(query):
        """Search for stock symbols with autocomplete"""
        if not query or len(query) < 2:
            return []
        
        try:
            # Yahoo Finance search API
            url = "https://query2.finance.yahoo.com/v1/finance/search"
            params = {
                "q": query,
                "quotesCount": 10,
                "newsCount": 0,
                "enableFuzzyQuery": False,
                "quotesQueryId": "tss_match_phrase_query"
            }
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            
            suggestions = []
            for quote in data.get('quotes', []):
                # Filter for Indian stocks (NSE)
                symbol = quote.get('symbol', '')
                if '.NS' in symbol or '.BO' in symbol:
                    suggestions.append({
                        'symbol': symbol.replace('.NS', '').replace('.BO', ''),
                        'name': quote.get('longname') or quote.get('shortname', ''),
                        'exchange': quote.get('exchange', ''),
                        'type': quote.get('quoteType', '')
                    })
            
            return suggestions[:10]
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    @staticmethod
    def fetch_candles(symbol, period):
        ticker = f"{symbol}{INDIAN_STOCK_SUFFIX}"
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        
        if data.empty:
            return None
        
        candles = []
        for index, row in data.iterrows():
            candles.append({
                "date": index.strftime("%Y-%m-%d"),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2),
                "volume": int(row['Volume'])
            })
            
        return candles
    
    @staticmethod
    def get_stock_info(symbol):
        ticker = f"{symbol}{INDIAN_STOCK_SUFFIX}"
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "symbol": symbol,
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "current_price": info.get("currentPrice", 0),
            "previous_close": info.get("previousClose", 0),
            "day_high": info.get("dayHigh", 0),
            "day_low": info.get("dayLow", 0),
            "52_week_high": info.get("fiftyTwoWeekHigh", 0),
            "52_week_low": info.get("fiftyTwoWeekLow", 0),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "avg_volume": info.get("averageVolume", 0)
        }
