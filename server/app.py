# server/app.py
from flask import request, jsonify
from flask_cors import CORS
from config import app, db
from sqlalchemy.exc import IntegrityError

# CORS config
CORS(app, supports_credentials=True)

# routes go here

