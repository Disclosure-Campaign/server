from flask import Flask, jsonify, request
from flask_cors import CORS

from server.src.APIs.index import APIs

app = Flask(__name__)
cors = CORS(app)

@app.route('/api/prediction', methods=['POST'])

@app.route('/data')

def request_data():
    params = request.args.to_dict()

    result = APIs['fetch_data'](params)

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to retrieve data from the API"}), 500

if __name__ == "__main__":
    app.run(debug=True)