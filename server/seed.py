# server/seed.py
from app import app, db
from models import Plant, Garden, CultivatePlants, FieldGuide, Player

def seed_plants():
    print("seeding plants...")
    plants = [
        Plant(name="Thyme", level=1),
        Plant(name="Carrot", level=2),
        Plant(name="Tulip", level=2)
    ]


def seed_gardens():
    gardens = [
        Garden(name="Home"),
        Garden(name="Farm"),
        Garden(name="Moon Garden")
    ]

def seed_cultivated():
    pass

def seed_field_guide():
    pass

def seed_players():
    pass

# Function to seed the database
def seed_database():
    with app.app_context():
        # Drop existing tables and create new ones
        db.drop_all()  
        db.create_all()
        
        # Seed the database with fake data
        #seed_plants(10)  # 10 users
        #seed_songs(20)  # 20 songs
        #seed_mixtapes(10)  # 10 mixtapes
        #seed_mixtape_items(30)  # 30 mixtape items

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()