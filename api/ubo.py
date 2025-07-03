# api/ubo.py
import json
from flask import Flask, request, jsonify
from handelsregister import main as hr_main

app = Flask(__name__)

@app.route('/api/ubo', methods=['POST'])
def ubo():
    body = request.get_json() or {}
    name = body.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Kein Name angegeben'}), 400

    try:
        # Call the CLI entry-point; capture its JSON output
        data = hr_main(['-s', name, '-so', 'all', '-f'])
        # hr_main should return a Python dict; if it prints JSON, parse it:
        if isinstance(data, str):
            data = json.loads(data)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
