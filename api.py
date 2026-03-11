"""
Local API server for testing
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import config

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/api/items')
def get_items():
    """Get all items"""
    try:
        with open(config.JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_website():
    """Serve the POS website"""
    return send_from_directory(config.TEMPLATES_DIR, 'index.html')

if __name__ == '__main__':
    print(f"🚀 Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)