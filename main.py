import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_city_coordinates(city_name):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data:
            print(f"Could not find {city_name}")
            return None, None
        
        return data[0]['lat'], data[0]['lon']
    
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        return None, None
    except:
        print("Something went wrong")
        return None, None