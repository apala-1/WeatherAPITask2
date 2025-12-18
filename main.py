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
    
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 401:
            print("API key invalid")
            return None
        
        return response.json()
    
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        return None
    except:
        print("Failed to get weather data")
        return None

def display_weather(weather_data):
    city = weather_data['city']['name']
    country = weather_data['city']['country']
    
    print(f"\nWeather forecast for {city}, {country}\n")
    
    forecasts = weather_data['list'][:8]
    
    for forecast in forecasts:
        date_time = forecast['dt_txt']
        temp = forecast['main']['temp']
        feels_like = forecast['main']['feels_like']
        humidity = forecast['main']['humidity']
        wind_speed = forecast['wind']['speed']
        description = forecast['weather'][0]['description']
        
        print(f"{date_time}")
        print(f"Temperature: {temp}°C (feels like {feels_like}°C)")
        print(f"Humidity: {humidity}%")
        print(f"Wind: {wind_speed} m/s")
        print(f"{description.capitalize()}\n")

def main():
    print("Weather Forecast App")
    
    city = input("\nEnter city name: ").strip()
    
    if not city:
        print("Please enter a city name")
        return
    
    print(f"Getting weather for {city}...")
    lat, lon = get_city_coordinates(city)
    
    if lat is None:
        return
    
    weather_data = get_weather(lat, lon)
    
    if weather_data is None:
        return
    
    display_weather(weather_data)

if __name__ == "__main__":
    main()