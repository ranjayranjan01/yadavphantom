from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import urllib.request
import json
from urllib.parse import unquote
import os

app = Flask(__name__)
CORS(app, origins=["https://web-production-33a3.up.railway.app", "http://localhost:5000"])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/<type>/<query>')
@cross_origin()
def api_proxy(type, query):
    try:
        query_value = unquote(query)
        print(f"API Call: {type} = {query_value}")
        
        api_url = f"http://dark-op.dev-is.xyz/?key=wasdark&{type}={query_value}"
        
        # Make request with headers
        req = urllib.request.Request(api_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            api_data = response.read().decode('utf-8')
            
        return jsonify(json.loads(api_data))
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
