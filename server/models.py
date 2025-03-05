from config import db, SerializerMixin, association_proxy
from sqlalchemy.orm import validates #python / app level validations
s

# Plant Model
class Plant(db.Model, SerializerMixin):
    __tablename__ = "plants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    # relationships
    cultivated = db.relationship("CultivatePlants", back_populates="plants")
    guide = db.relationship("FieldGuide", back_populates="plants")
    #serializer
    serializer_rules = ('cultivated', 'guide', '-cultivated.plants', '-guide.plants')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level
        }


# Garden Model
class Garden(db.Model, SerializerMixin):
    __tablename__ = "gardens"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="Garden")
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    # relationships
    cultivated = db.relationship("CultivatePlants", back_populates="gardens")
    player = db.relationship("Player", back_populates="gardens")
    # serializer
    serializer_rules = ('cultivated', 'player', 'cultivated.gardens', '-player.gardens')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'player_id': self.player_id
        }


# CultivatePlants Model
class CultivatePlants(db.Model, SerializerMixin):
    __tablename__ = "cultivated_plants"
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    garden_id = db.Column(db.Integer, db.ForeignKey('gardens.id'), nullable=False)
    x = db.Column(db.Integer, nullable=False) # Store x coordinate of planting
    y = db.Column(db.Integer, nullable=False) # Store y coordinate of planting

    # relationships
    plants = db.relationship("Plant", back_populates="cultivated")
    gardens = db.relationship("Garden", back_populates="cultivated")

    # serializer
    serializer_rules =('plants', 'gardens', '-plants.cultivated', '-gardens.cultivated')

    def to_dict(self):
        return {
            'id': self.id,
            'plant': self.plants.to_dict() if self.plants else None,
            'garden': self.gardens.to_dict() if self.gardens else None,
            'x'  : self.x,
            'y' : self.y
        }


# FieldGuide Model
class FieldGuide(db.Model, SerializerMixin):
    __tablename__ = "field-guide"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False, unique=True)
    # relationships
    plants = db.relationship("Plant", back_populates="guide")
    # serializer
    serializer_rules= ('plants', '-plants.guide')

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'plant_id': self.plant_id,
            'plant': self.plants.to_dict() if self.plants else None
        }


# Player Model
class Player(db.Model, SerializerMixin):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default="Player")
    # relationships
    gardens = db.relationship("Garden", back_populates="player")
    # serializer
    serializer_rules = ('gardens', '-gardens.player')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gardens': [garden.to_dict() for garden in self.gardens]
        }
