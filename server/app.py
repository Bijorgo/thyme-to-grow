# server/app.py
from flask import request, jsonify
from flask_cors import CORS
from config import app, db, SerializerMixin
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api
# Import models
from models import Plant, Garden, CultivatePlants, FieldGuide, Player

# Issues to come back to:
    # properly serialize relationships (ex cultivatedPlants=> plants and gardens)
    # .to_dict isnt turning yellow
    # validations 
    # specify parameters when patch and delete require an id to locate ( add this in api.add .... /players/<int:player_id>)
    # player not needing to be unique may be an issue

# Configs
CORS(app, supports_credentials=True)
api = Api(app)

#@app.get("/")
#def index():
#    return jsonify({"message" : "Welcome to the Thyme to Grow API"})

class Index(Resource):
    def get(self):
        return { "message" : "Welcome to the Thyme to Grow API" }
    
class PlantResource(Resource):
    def get(self):
        plants = Plant.query.all()
        if not plants:
            return { "plants": [] }, 200
        plant_list = [{ "name" : plant.name} for plant in plants]
        return { "plants": plant_list }, 200

class GardenResource(Resource):
    def get(self):
        gardens = Garden.query.all()
        if not gardens:
            return { "gardens": [] }, 200
        
        garden_list = [garden.to_dict() for garden in gardens]
        return { "gardens": garden_list }, 200
    #def post(self):
        #pass
    #def patch(self):
        #pass

class CultivatedPlantsResource(Resource):
    def get(self):
        cultivatedPlants = CultivatePlants.query.all()
        if not cultivatedPlants:
            return { "planted": [] }, 200
        currentlyPlanted = [{ "plant": planted.plants, "garden": planted.garden} for planted in cultivatedPlants]
        return { "cultivated-plants": currentlyPlanted }, 200
    def post(self):
        pass
    def delete(self):
        pass

class FieldGuideResource(Resource):
    def get(self):
        all_plants = FieldGuide.query.all()
        if not all_plants:
            return { "message": "Error: no plants in database" }, 404
        plant_list = [{ "plant": plant.plants} for plant in all_plants]
        return { "plants": plant_list}, 200
    def patch(self):
        # toggle status found /not yet found
        pass

class PlayerResource(Resource):
    def get(self):
        players = Player.query.all()
        return {"players": [player.to_dict() for player in players]}, 200
    
    def post(self):
        data = request.get_json()
        if not data or "name" not in data:
            return {"Error": "Name is required"}, 400
        try:
            new_player = Player(name=data["name"])
            db.session.add(new_player)
            db.session.commit()
            return (new_player.to_dict()), 201
        except Exception as exc:
            return { "Error": str(exc) }, 400
    def patch(self, player_id):
        data = request.get_json()
        player = Player.query.get(player_id)
        if not player:
            return { "Error": "Player not found" }, 404
        if "name" in data:
            player.name = data["name"]
        try:
            db.session.commit()
            return player.to_dict(), 200
        except Exception as exc:
            db.session.rollback()
            return {"error": str(exc)}, 500
        
    def delete(self, player_id):
        player = Player.query.get(player_id)
        if not player:
            return {"error": "Player not found"}, 404
        try:
            db.session.delete(player)
            db.session.commit()
            return {"message": "Player deleted successfully"}, 200
        except Exception as exc:
            db.session.rollback()
            return {"error": str(exc)}, 500

# `api.add_resource(<Resource>, <endpoint>)`
# maps the methods in <Resource> to <endpoint>.
api.add_resource(Index, "/")
api.add_resource(PlantResource, "/plants")
api.add_resource(GardenResource, "/gardens")
api.add_resource(CultivatedPlantsResource, "/cultivated-plants")
api.add_resource(FieldGuideResource, "/field-guide")
api.add_resource(PlayerResource, "/player")

