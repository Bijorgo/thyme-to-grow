# server/seed.py
from app import app, db
from models import Plant, Garden, CultivatePlants, FieldGuide, Player

def seed_plants():
    print("seeding plants...")
    plants = [
        Plant(name="Thyme", level=1),
        Plant(name="Carrot", level=2),
        Plant(name="Tulip", level=2),
        #Plant(name="True Tester", level=1) # for testing true option in field guide 
    ]
    db.session.add_all(plants)
    db.session.commit()
    print(f"{len(plants)} plants seeded! ")

def seed_gardens():
    print("seeding gardens...")
    gardens = [
        #Garden(name="Home", player_id=None),
        Garden(name="Farm", player_id=1),
        Garden(name="Moon Garden", player_id=1)
    ]
    db.session.add_all(gardens)
    db.session.commit()
    print(f"{len(gardens)} gardens seeded!")

#def seed_cultivated():
    # This is for dev testing only
    #print("seeding cultivated plants is for dev testing only. If this was not intended, please stop and adjust.")
    #print("seeding cultivated plants...")
    #plants_from_db = Plant.query.all()
    #if not plants_from_db:
        #print("no plants available to seed, skipping seeding...")
        #return
    #gardens_from_db = Garden.query.all()
    #if not gardens_from_db:
        #print("no gardens available to seed, skipping seeding...")
        #return
    #cultivated_entries = []
    # assign every plant to every garden, tested and works
    #for garden in gardens_from_db:
        #for plant in plants_from_db: # both a garden id and plant id are required to create an entry
            #cultivated_entries.append(CultivatePlants(plant_id=plant.id, garden_id=garden.id))
    #db.session.add_all(cultivated_entries)
    #db.session.commit()
    #print(f"{len(cultivated_entries)} entries seeded!")

def seed_field_guide():
    print("seeding field guide...")
    plants = Plant.query.all()
    if not plants:
        print("No plants found, skipping seeding...")
        return
    field_guide_entries = []

    for plant in plants:
        if plant.name == "True Tester":
            field_guide_entries.append(FieldGuide(plant_id=plant.id, status=True))
        else:
            field_guide_entries.append(FieldGuide(status=False, plant_id=plant.id))

    db.session.add_all(field_guide_entries)
    db.session.commit()
    print(f"{len(field_guide_entries)} entries seeded!")

def seed_players():
    print("seeding players...")
    # Create players
    players=[
        Player(name="Fern"),
        Player(name="Fernando")
    ]

    for player in players:

        db.session.add(player)
        db.session.commit() # commit each player to db to create id

        # Check if player has Home garden
        home_garden = Garden.query.filter_by(name="Home", player_id=player.id).first()

        # If not, create Home garden
        if not home_garden:
            home_garden = Garden(name="Home", player_id=player.id)
            db.session.add(home_garden)
            db.session.commit() # commit to save Home garden to db

        # Assign Home garden to pleyer
        player.garden_id = home_garden.id
        db.session.commit()
    print(f"{len(players)} players seeded with Home garden!")

# Function to seed the database
def seed_database():
    with app.app_context():
        # Drop existing tables and create new ones
        print("dropping all tables...")
        db.drop_all()  
        print("creating all tables...")
        db.create_all()
        
        # Seed the database with data
        seed_plants() 
        seed_gardens()
        seed_cultivated() # for dev testing only
        seed_field_guide() # make sure to call this AFTER calling seed_plants()
        seed_players() # this should be seeded AFTER gardens, but may still work if it is not

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()