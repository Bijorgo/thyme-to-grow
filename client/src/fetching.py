# src/fetching.py

import requests

BASE_URL = "http://127.0.0.1:5000" 

ENDPOINTS = [
    "/plants",
    "/gardens",
    "/cultivated-plants",
    "/field-guide",
    "/player"
]

def get_players():
    try:
        response = requests.get('http://127.0.0.1:5000/player')
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as exc:
        print(f"error fetching{exc}")
        return []
    
def get_plants():
    try:
        response = requests.get('http://127.0.0.1:5000/plants')
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as exc:
        print(f"error fetching{exc}")
        return []
    
def get_gardens():
    try:
        response = requests.get('http://127.0.0.1:5000/gardens')
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as exc:
        print(f"error fetching{exc}")
        return []
    
def get_cultivated():
    try:
        response = requests.get('http://127.0.0.1:5000/cultivated-plants')
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as exc:
        print(f"error fetching{exc}")
        return []
    
def get_field_guide():
    try:
        response = requests.get('http://127.0.0.1:5000/field-guide')
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as exc:
        print(f"error fetching{exc}")
        return []