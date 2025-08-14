from flask import Flask
from flask_cors import CORS
import os

from app import create_app

app = create_app()

CORS(app)

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'production':
        app.run()
    else:
        app.run(host='0.0.0.0', port=5001, debug=True)