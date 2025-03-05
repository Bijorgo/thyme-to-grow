# src/fetching.py
import requests

# ACTIVE IN LEVEL
def get_players():
    try:
        response = requests.get('http://127.0.0.1:5000/player')
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as exc:
        print(f"error fetching{exc}")
        return []

# ACTIVE IN LEVEL
def get_plants():
    response = requests.get("http://127.0.0.1:5000/plants")
    
    if response.status_code == 200:
        return response.json()["plants"] # Need to return a list 
    else:
        print("Error fetching plants:", response.text)
        return []
    
