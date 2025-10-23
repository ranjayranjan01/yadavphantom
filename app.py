from flask import Flask, render_template, jsonify
from flask_cors import CORS
import urllib.request
import json
from urllib.parse import unquote
import os
import ssl

app = Flask(__name__)
CORS(app)

# SSL context create karo for HTTPS calls
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/<type>/<query>')
def api_proxy(type, query):
    try:
        query_value = unquote(query)
        print(f"🔍 API Call: {type} = {query_value}")
        
        # HTTPS use karo (agar available ho)
        api_url = f"https://dark-op.dev-is.xyz/?key=wasdark&{type}={query_value}"
        
        # Try HTTPS first
        try:
            req = urllib.request.Request(api_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                api_data = response.read().decode('utf-8')
                
        except:
            # Fallback to HTTP
            api_url_http = f"http://dark-op.dev-is.xyz/?key=wasdark&{type}={query_value}"
            req = urllib.request.Request(api_url_http, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=10) as response:
                api_data = response.read().decode('utf-8')
            
        return jsonify(json.loads(api_data))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

