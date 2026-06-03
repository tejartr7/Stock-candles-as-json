import json
from search_engine import SearchEngine

def main():
    engine = SearchEngine()
    
    # Get user input
    symbol = input("Enter stock symbol (e.g., RELIANCE, TCS, INFY): ").upper()
    timeline = input("Enter timeline (30d/60d/90d): ")
    
    print(f"\nFetching data for {symbol}...")
    result = engine.search(symbol, timeline)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    data = result['result']
    filepath = result['saved_to']
    
    # Display summary
    print(f"\n{'='*60}")
    print(f"Stock: {data['stock_info']['name']}")
    print(f"Symbol: {symbol}")
    print(f"Sector: {data['stock_info']['sector']}")
    print(f"{'='*60}")
    print(f"\nCurrent Price: ₹{data['price_summary']['current_price']}")
    print(f"Period Change: ₹{data['price_summary']['price_change']} ({data['price_summary']['price_change_percentage']}%)")
    print(f"Period High: ₹{data['price_summary']['period_high']}")
    print(f"Period Low: ₹{data['price_summary']['period_low']}")
    print(f"\nTotal Candles: {data['metadata']['total_candles']}")
    print(f"\n{'='*60}")
    print(f"✓ Data saved to: {filepath}")
    print(f"{'='*60}")
    
    # Show AI prompt
    print("\n📊 AI Analysis Prompt:")
    print(json.dumps(data['ai_analysis_prompt'], indent=2))
    print(f"\n💡 Upload '{filepath}' to any AI tool (ChatGPT, Claude, Gemini) for trading analysis!")

if __name__ == "__main__":
    main()
