from config import db, SerializerMixin, association_proxy
from sqlalchemy.orm import validates #python / app level validations

# constraints: nullable, defaults
# validations: data types, data structures

# Plant
class Plant(db.Model):
    __tablename__="plants"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    #type = db.Column(db.String)
    #rarity = db.Column(db.String)
    # Relationships
    cultivated = db.relationship("CultivatePlants", back_populates="plants")
    guide = db.relationship("FieldGuide", back_populates="plants")
    # Serialize rules
    serializer_rules = ('cultivated', 'guide', '-cultivated.plants', '-guide.plants')
    # Validations
    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Plant name must be a non-empty string.")
        return value
    
    @validates("level")
    def validate_level(self, key, value):
        if not isinstance(value, int):
            raise ValueError("Level must be assigned integer")
        return value

# Garden
class Garden(db.Model):
    __tablename__="gardens"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="Garden")
    #location = db.Column(db.String)
    # Relationships
    cultivated = db.relationship("CultivatePlants", back_populates="gardens")
    player = db.relationship("Player", back_populates="gardens")
    plants = association_proxy('cultivated-plants', 'plants') # hyphen?
    # Serialize rules
    serializer_rules = ('cultivated', 'player', '-cultivated.gardens', '-player.gardens')
    # Validations
    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Gardemn n name must be a non-empty string.")
        return value

# CultivatePlants
# Tracks currently planted plants. Should delete relationship once harvested
class CultivatePlants(db.Model):
    __tablename__="cultivated-plants"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    garden_id = db.Column(db.Integer, db.ForeignKey('gardens.id'), nullable=False)
    # Relationships
    plants = db.relationship("Plant", back_populates="cultivated")
    gardens = db.relationship("Garden", back_populates="cultivated")
    # Serialize rules
    serializer_rules = ('plants', 'gardens', '-plants.cultivated', '-gardens.cultivated')
    # Validations
    @validates("plant_id")
    def validate_plant_id(self, key, value):
        if not value: # Check for None value
            raise ValueError("Plant id required")
        if not db.session.get(Plant, value):  # Ensure plant exists
            raise ValueError("Plant does not exist.")
        return value
    
    @validates("garden_id")
    def validate_garden_id(self, key, value):
        if not value: # Check for None value
            raise ValueError("Garden id required")
        if not db.session.get(Garden, value):  # Ensure garden exists
            raise ValueError("Garden does not exist.")
        return value

# Field Guide
class FieldGuide(db.Model):
    __tablename__="field-guide"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default="False") # default to false, false is stored as 0, true is stored as 1
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False, unique=True) # a plant can only show up once 
    # Relationships
    plants = db.relationship("Plant", back_populates="guide")
    # Serialize rules
    serializer_rules = ('plants', '-plants.guide')

# Player
class Player(db.Model):
    __tablename__="players"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default="Player")
    garden_id = db.Column(db.Integer, db.ForeignKey('gardens.id'), nullable=True)
    # Relationships
    gardens = db.relationship("Garden", back_populates="player")
    # Serializer rules
    serializer_rules = ('gardens', '-gardens.player')
