import json
import os
from datetime import datetime
from stock_api import StockAPI
from config import VALID_PERIODS, OUTPUT_DIR

class SearchEngine:
    def __init__(self):
        # Create output directory if not exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    def search(self, symbol, timeline="30d"):
        """Search and fetch stock candles with AI-ready format"""
        if timeline not in VALID_PERIODS:
            return {"error": f"Invalid timeline. Use: {list(VALID_PERIODS.keys())}"}
        
        # Get stock info
        info = StockAPI.get_stock_info(symbol)
        
        # Fetch candles
        period = VALID_PERIODS[timeline]
        candles = StockAPI.fetch_candles(symbol, period)
        
        if not candles:
            return {"error": f"No data found for {symbol}"}
        
        # Calculate technical indicators
        latest_candle = candles[-1]
        price_change = latest_candle['close'] - candles[0]['close']
        price_change_pct = (price_change / candles[0]['close']) * 100
        
        # AI-ready structured data
        result = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "symbol": symbol,
                "timeline": timeline,
                "total_candles": len(candles)
            },
            "stock_info": info,
            "price_summary": {
                "current_price": latest_candle['close'],
                "period_start_price": candles[0]['close'],
                "period_high": max(c['high'] for c in candles),
                "period_low": min(c['low'] for c in candles),
                "price_change": round(price_change, 2),
                "price_change_percentage": round(price_change_pct, 2)
            },
            "candles": candles,
            "ai_analysis_prompt": {
                "question": f"Based on the {timeline} candlestick data for {info['name']} ({symbol}), please analyze:",
                "requirements": [
                    "Is this suitable for swing trading or intraday trading?",
                    "What should be the recommended investment amount?",
                    "What should be the entry price (opening amount)?",
                    "What are the stop-loss and target levels?",
                    "What is the risk-reward ratio?"
                ]
            }
        }
        
        # Save to JSON file
        filename = f"{symbol}_{timeline}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        return {
            "result": result,
            "saved_to": filepath
        }
