# server/app.py
from flask_cors import CORS
from config import app, db

# CORS config
CORS(app, supports_credentials=True)

# routes go here

