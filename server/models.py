from config import db, SerializerMixin, association_proxy
from sqlalchemy.orm import validates #python / app level validations

# constraints: nullable, defaults
# validations: data types, data structures

# Plant
class Plant(db.Model):
    __tablename__="plants"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    level = db.Column(db.Integer)
    #type = db.Column(db.String)
    #rarity = db.Column(db.String)
    # Relationships
    cultivated = db.relationship("CultivatedPlants", back_populates="plants")


# Garden
class Garden(db.Model):
    __tablename__="gardens"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    #location = db.Column(db.String)
    # Relationships
    cultivated = db.relationship("CultivatedPlants", back_populates="gardens")


# CultivatedPlants
class CultivatePlants(db.Model):
    __tablename__="cultivated-plants"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'))
    garden_id = db.Column(db.Integer, db.ForeignKey('gardens.id'))
    # Relationships
    plants = db.relationship("Plant", back_populates="")
    gardens = db.relationship("Garden", back_populates="cultivated")

# Field Guide
class FieldGuide(db.Model):
    __tablename__="field-guide"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean) # default to false
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'))
    # Relationships

# Character
class Character(db.Model):
    __tablename__="characters"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
