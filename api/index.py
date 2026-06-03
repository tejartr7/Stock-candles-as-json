import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify, send_file
from stock_api import StockAPI
from search_engine import SearchEngine

app = Flask(__name__, template_folder='../templates')
engine = SearchEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '')
    suggestions = StockAPI.search_symbols(query)
    return jsonify(suggestions)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    symbol = data.get('symbol', '').upper()
    timeline = data.get('timeline', '30d')
    
    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400
    
    result = engine.search(symbol, timeline)
    
    if "error" in result:
        return jsonify(result), 404
    
    return jsonify({
        "data": result['result'],
        "filepath": result['saved_to']
    })

@app.route('/download/<path:filename>')
def download(filename):
    filepath = os.path.join('..', filename)
    return send_file(filepath, as_attachment=True)
