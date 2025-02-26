# server/app.py
from flask import request, jsonify
from flask_cors import CORS
from config import app, db, SerializerMixin
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api
# Import models
from models import Plant, Garden, CultivatePlants, FieldGuide, Player


# Issues to come back to:
    # properly serioalize relationships (ex cultivatedPlants=> plants and gardens)
    # .to_dict isnt turning yellow
    # validations 

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
    def get(self):
        plants = Plant.query.all()
        if not plants:
            return { "message": "No plants found"}, 404
        plant_list = [{ "name" : plant.name} for plant in plants]
        return { "plants": plant_list}, 200

class GardenResource(Resource):
    def get(self):
        gardens = Garden.query.all()
        if not gardens:
            return { "message": "No gardens found"}, 404
        garden_list = [{ "name": garden.name} for garden in gardens]
        return { "gardens": garden_list}, 200
    #def post(self):
        #pass
    #def patch(self):
        #pass

class CultivatedPlantsResource(Resource):
    def get(self):
        cultivatedPlants = CultivatePlants.query.all()
        if not cultivatedPlants:
            return { "message": "No plants currently planted"}, 404
        currentlyPlanted = [{ "plant": planted.plants, "garden": planted.garden} for planted in cultivatedPlants]
        return { "cultivated-plants": currentlyPlanted}, 200
    def post(self):
        pass
    def delete(self):
        pass

class FieldGuideResource(Resource):
    def get(self):
        all_plants = FieldGuide.query.all()
        if not all_plants:
            return { "message": "Error: no plants in database"}, 404
        plant_list = [{ "plant": plant.plants} for plant in all_plants]
        return { "plants": plant_list}, 200

class PlayerResource(Resource):
    def get(self):
        players = Player.query.all()
        if not players:
            return { "message": "Please create a character"}
        player_list = [{ "name": player.name, "gardens": player.gardens} for player in players]
        return{ "player": player_list}, 200
    def post(self):
        data = request.json
        try:
            new_player = Player(name=data["name"])
            db.session.add(new_player)
            db.session.commit()
            return (new_player.to_dict()), 201
        except Exception as exc:
            return { "Error": str(exc)}, 400
    def patch(self):
        pass
    def delete(self):
        pass

# `api.add_resource(<Resource>, <endpoint>)`
# maps the methods in <Resource> to <endpoint>.
api.add_resource(Index, "/")
api.add_resource(PlantResource, "/plants")
api.add_resource(GardenResource, "/gardens")
api.add_resource(CultivatedPlantsResource, "/cultivated-plants")
api.add_resource(FieldGuideResource, "/field-guide")
api.add_resource(PlayerResource, "/player")

