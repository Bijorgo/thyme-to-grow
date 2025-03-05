# Thyme to Grow

Thyme to Grow is a gardening-themed game built using **Pygame** for the frontend and **Flask** with **SQLAlchemy** for the backend. Players can manage their virtual gardens, select different players, and interact with garden elements in a fun and engaging way.

## Features
- **Player Selection**: Choose from different players to access their unique gardens.
- **Garden Management**: View and select gardens, with interactive elements.
- **Dynamic Game Levels**: Fetch and display garden data dynamically.

## Technologies Used
### Backend:
- **Flask** (API & server-side logic)
- **Flask-SQLAlchemy** (Database management)
- **Flask-Migrate** (Database migrations)
- **Requests** (Fetching garden data from the backend)

### Frontend:
- **Pygame-CE** (Game UI & rendering)
- **Custom UI Elements** (Buttons, sprites, backgrounds)

## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/thyme-to-grow.git
cd thyme-to-grow
```

### 2. Set Up Backend
Navigate to the `server` directory and install dependencies:
```sh
cd server
pipenv install
pipenv shell  # Activate virtual environment
python seed.py # Seed databse with plant and garden information
flask db upgrade  # Run database migrations
flask run  # Start Flask server
```

### 3. Set Up Frontend
Navigate to the `client` directory and install dependencies:
```sh
cd ../client
pipenv install
pipenv shell  # Activate virtual environment
python main.py  # Start the game
```

## Usage
- Run `flask run` in the `server` directory to start the backend.
- Run `python main.py` in the `client` directory to launch the game.
- Select a **player** from the menu.
- Choose a **garden** to manage and interact with.
- Use the arrow keys to move your player.
- Use `p` key to plant a plant.
- Use `h` key to harvest a plant.
- Press and hold `m` key, move your player, then release `m` key to move a plant.
- Use the mouse to click "Main Menu" to return to main menu

## Project Structure
```
thyme-to-grow/
│── client/                # Pygame frontend
│   ├── src/               # Game assets & logic
|   ├── config.py          # Screen/window configurations 
│   ├── main.py            # Main entry point for the game
│── server/                # Flask backend
│   ├── app.py             # Main Flask app, routes
│   ├── models.py          # Database models
│   ├── config.py          # Congigurations
│── README.md              # Project documentation
```


## Pixel Art
All pixel art was created by me

This project was created as a capstone project for 
Flatiron School Software Engineering program 


