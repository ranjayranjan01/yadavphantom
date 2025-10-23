from flask import Flask, render_template
import urllib.request
import json
from urllib.parse import unquote
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/<type>/<query>')
def api_proxy(type, query):
    try:
        query_value = unquote(query)
        api_url = f"http://dark-op.dev-is.xyz/?key=wasdark&{type}={query_value}"
        
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req, timeout=10) as response:
            api_data = response.read()
            
        return app.response_class(
            response=api_data,
            status=200,
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
