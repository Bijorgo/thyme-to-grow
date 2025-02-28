# server/app.py
from flask import request, jsonify
from flask_cors import CORS
from config import app, db, SerializerMixin
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api
# Import models
from models import Plant, Garden, CultivatePlants, FieldGuide, Player

# Configs
CORS(app, supports_credentials=True)
api = Api(app)

# Index
class Index(Resource):
    def get(self):
        return { "message" : "Welcome to the Thyme to Grow API" }

# Plant Resource
class PlantResource(Resource):
    def get(self):
        plants = Plant.query.all()
        if not plants:
            return { "plants": [] }, 200
        plant_list = [{ "name" : plant.name} for plant in plants]
        return { "plants": plant_list }, 200

# Garden Resource
class GardenResource(Resource):
    def get(self, garden_id=None, player_id=None):
        if garden_id:  # Fetch a single garden by ID
            garden = Garden.query.get(garden_id)
            if not garden:
                return { "error": "Garden not found" }, 404
            return garden.to_dict(), 200
        
        if player_id:  # if ID is provided, fetch for that player
            player = Player.query.get(player_id)
            if not player:
                return { "error": "Player not found" }, 404
            gardens = Garden.query.filter_by(player_id=player.id).all()

        else:
            gardens = Garden.query.all()  # Fetch all gardens

        garden_list = [garden.to_dict() for garden in gardens]
        return { "gardens": garden_list }, 200
    
    def post(self):
        data = request.get_json()
        
        # Ensure player and garden are provided in the request
        player_id = data.get('player_id')
        garden_id = data.get('garden_id')
        plant_id = data.get('plant_id')

        if not player_id or not garden_id or not plant_id:
            return {"error": "Player ID, Garden ID, and Plant ID are required"}, 400
        
        player = Player.query.get(player_id)
        if not player:
            return {"error": "Player not found"}, 404
        
        garden = Garden.query.get(garden_id)
        if not garden:
            return {"error": "Garden not found"}, 404
        
        plant = Plant.query.get(plant_id)
        if not plant:
            return {"error": "Plant not found"}, 404

        # Create a new CultivatePlants record to associate the plant with the garden
        new_cultivation = CultivatePlants(plant_id=plant.id, garden_id=garden.id)
        db.session.add(new_cultivation)
        db.session.commit()

        return {"message": "Seed planted successfully"}, 201

# Cultivated Plants Resource
class CultivatedPlantsResource(Resource):
    def get(self):
        cultivatedPlants = CultivatePlants.query.all()
        if not cultivatedPlants:
            return { "planted": [] }, 200
        currentlyPlanted = [
            { 
                "plant": planted.plants.to_dict(), 
                "garden": planted.gardens.to_dict()
            } 
            for planted in cultivatedPlants
        ]
        return { "cultivated-plants": currentlyPlanted }, 200
    
    def post(self):
        data = request.get_json()
        
        # Check for missing data
        if not data or not all(key in data for key in ["player_id", "garden_id", "plant_id"]):
            return {"error": "player_id, garden_id, and plant_id are required"}, 400
        
        player_id = data["player_id"]
        garden_id = data["garden_id"]
        plant_id = data["plant_id"]

        # Check if player, garden, and plant exist
        player = Player.query.get(player_id)
        garden = Garden.query.get(garden_id)
        plant = Plant.query.get(plant_id)

        if not player or not garden or not plant:
            return {"error": "Invalid player, garden, or plant"}, 404

        # Create new cultivated plant entry
        cultivated_plant = CultivatePlants(plant_id=plant_id, garden_id=garden_id)
        db.session.add(cultivated_plant)
        try:
            db.session.commit()
            return cultivated_plant.to_dict(), 201  # Return created cultivated plant
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        
    def patch(self):
        pass
    
    def delete(self):
        pass

# Field Guide Resource
class FieldGuideResource(Resource):
    def get(self):
        all_plants = FieldGuide.query.all()
        if not all_plants:
            return { "message": "Error: no plants in database" }, 404
        
        plant_list = [{ "plant": plant.plants.to_dict() } for plant in all_plants]
        return { "plants": plant_list}, 200
    
    def patch(self):
        # toggle status found/not yet found
        pass

# Player Resource
class PlayerResource(Resource):
    def get(self, player_id=None):
        if player_id:
            player = Player.query.get(player_id)
            if not player:
                return {"error": "Player not found"}, 404
            return player.to_dict(), 200
        
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
api.add_resource(GardenResource, "/gardens", "/gardens/<int:garden_id>", "/player/<int:player_id>/gardens")
api.add_resource(CultivatedPlantsResource, "/cultivated-plants")
api.add_resource(FieldGuideResource, "/field-guide")
api.add_resource(PlayerResource, "/player", "/player/<int:player_id>")
