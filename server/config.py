# server/config.py

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.exc import IntegrityError
#from flask_restful import Api, Resource

# init flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///thyme-to-grow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_COMPACT'] = False # allow json response to be verbose

# init SQLAlchemy
db = SQLAlchemy(app)

# init Alembic
migrate = Migrate(app, db)