# server/app.py
from flask import request, jsonify
from flask_cors import CORS
from config import app, db
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api

# Configs
CORS(app, supports_credentials=True)
api = Api(app)

#@app.get("/")
#def index():
#    return jsonify({"message" : "Welcome to the Thyme to Grow API"})

class Index(Resource):
    def get(self):
        return {"message" : "Welcome to the Thyme to Grow API"}
    
class PlantResource(Resource):
    pass

class GardenResource(Resource):
    pass

class CultivatedPlantsResource(Resource):
    pass

class FieldGuideResource(Resource):
    pass

class PlayerResource(Resource):
    pass

# `api.add_resource(<Resource>, <endpoint>)`
# maps the methods in <Resource> to <endpoint>.
api.add_resource(Index, "/")
api.add_resource(PlantResource, "/plants")
api.add_resource(GardenResource, "/gardens")
api.add_resource(CultivatedPlantsResource, "/cultivated-plants")
api.add_resource(FieldGuideResource, "/field-guide")
api.add_resource(PlayerResource, "/player")

