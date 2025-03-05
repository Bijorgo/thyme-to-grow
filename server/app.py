# server/app.py
from flask import request, jsonify
from flask_cors import CORS
from config import app, db, SerializerMixin
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api
# Import models
from models import Plant, Garden, CultivatePlants, FieldGuide, Player

# Note: after switching to flask restful, jsonify() may be causing problems 

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
        plant_list = [{ "id" : plant.id, "name" : plant.name, "level" : plant.level} for plant in plants]
        return { "plants": plant_list }, 200

# Garden Resource
class GardenResource(Resource):
    def get(self, garden_id=None, player_id=None):

        # Fetch by only garden id
        if garden_id:  # Fetch a single garden by ID
            garden = Garden.query.get(garden_id)
            if not garden:
                return { "error": "Garden not found" }, 404
            return garden.to_dict(), 200
        
        # Fetch list of gardens associated with a player_id
        if player_id:  # if ID is provided, fetch for that player
            player = Player.query.get(player_id)
            if not player:
                return { "error": "Player not found" }, 404
            gardens = Garden.query.filter_by(player_id=player.id).all()

        # Fetch all gardens
        else:
            gardens = Garden.query.all()  

        # Return a list of gardens
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
    def get(self, cultivated_plant_id=None):
        # Fetch by specific id
        if cultivated_plant_id:
            cultivated_plant = CultivatePlants.query.get(cultivated_plant_id)
            if not cultivated_plant:
                return jsonify({"error": "Cultivation record not found"}), 404
            return cultivated_plant.to_dict(), 200
        
        # Fetch all entries
        else:
            cultivated_plants = CultivatePlants.query.all()
            if not cultivated_plants:
                return { "planted": [] }, 200 # Return empty list, not error
            # List of plant objects 
            currentlyPlanted = [
                { 
                    "id" : planted.id,
                    "plant": planted.plants.to_dict(), # Convert objects
                    "garden": planted.gardens.to_dict(),
                    "x": planted.x,
                    "y": planted.y
                } 
                for planted in cultivated_plants
            ]
            return { "cultivated-plants": currentlyPlanted }, 200 # This should be a list
        
    def post(self):
        data = request.get_json()
        
        # Check for missing data
        if not data or not all(key in data for key in ["player_id", "garden_id", "plant_id", "x", "y"]):
            return {"error": "player_id, garden_id, and plant_id, and coordinates are required"}, 400
        
        player_id = data["player_id"]
        garden_id = data["garden_id"]
        plant_id = data["plant_id"]
        x = data["x"]
        y = data["y"]

        # Check if player, garden, and plant exist
        player = Player.query.get(player_id)
        garden = Garden.query.get(garden_id)
        plant = Plant.query.get(plant_id)

        if not player or not garden or not plant:
            return {"error": "Invalid player, garden, or plant"}, 404

        # Create new cultivated plant entry
        cultivated_plant = CultivatePlants(plant_id=plant_id, garden_id=garden_id, x=x, y=y)
        db.session.add(cultivated_plant)
        try:
            db.session.commit()
            # Return structured 
            return {
            "id": cultivated_plant.id,
            "plant": cultivated_plant.plants.to_dict(),
            "garden": cultivated_plant.gardens.to_dict(),
            "x": cultivated_plant.x,
            "y": cultivated_plant.y
        }, 201

        except Exception as exc:
            db.session.rollback()
            return {"error": str(exc)}, 500
        
    def patch(self, cultivated_plant_id):
        # Get the request data
        data = request.get_json()

        # Fetch the cultivated plant by ID
        cultivated_plant = CultivatePlants.query.get(cultivated_plant_id)
        if not cultivated_plant:
            return {"error": "Cultivation record not found"}, 404
        
        # Update the coordinates if they are provided
        if 'x' in data:
            cultivated_plant.x = data['x']
        if 'y' in data:
            cultivated_plant.y = data['y']
        
        try:
            db.session.commit()
            # Return the updated object in the response
            return cultivated_plant.to_dict(), 200
        except Exception as exc:
            db.session.rollback()
            return {"error": str(exc)}, 500
    
    def delete(self, cultivated_plant_id):
        # Fetch based on plant_id
        plant = CultivatePlants.query.get(cultivated_plant_id)

        if plant is None:
            return {"error": "Plant not found"}, 404
        
        try:
            # Delete plant
            db.session.delete(plant)
            db.session.commit()
            return {"message": "ID deleted"}, 200 #Sucess
        
        except Exception as exc:
            db.session.rollback()
            return {"error": str(exc)}, 500

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
api.add_resource(CultivatedPlantsResource, "/cultivated-plants", "/cultivated-plants/<int:cultivated_plant_id>")
api.add_resource(FieldGuideResource, "/field-guide")
api.add_resource(PlayerResource, "/player", "/player/<int:player_id>")
