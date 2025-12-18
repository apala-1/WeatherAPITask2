import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_city_coordinates(city_name):
    """Get latitude and longitude from city name"""
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data:
            print(f"City '{city_name}' not found!")
            return None, None
        
        return data[0]['lat'], data[0]['lon']
    
    except requests.exceptions.ConnectionError:
        print("No internet connection!")
        return None, None
    except:
        print("Error finding city!")
        return None, None

def get_weather(lat, lon):
    """Fetch weather data from API"""
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 401:
            print("Invalid API key!")
            return None
        
        return response.json()
    
    except requests.exceptions.ConnectionError:
        print("No internet connection!")
        return None
    except:
        print("Error fetching weather!")
        return None

def display_weather(weather_data):
    """Print weather information nicely"""
    
    # Get city name
    city = weather_data['city']['name']
    country = weather_data['city']['country']
    print(f"\n{'='*50}")
    print(f"Weather Forecast for {city}, {country}")
    print(f"{'='*50}\n")
    
    # Show first 8 forecasts (24 hours, every 3 hours)
    forecasts = weather_data['list'][:8]
    
    for forecast in forecasts:
        # Extract data
        date_time = forecast['dt_txt']
        temp = forecast['main']['temp']
        feels_like = forecast['main']['feels_like']
        humidity = forecast['main']['humidity']
        wind_speed = forecast['wind']['speed']
        description = forecast['weather'][0]['description']
        
        # Print formatted output
        print(f"Date/Time: {date_time}")
        print(f"Temperature: {temp}°C (Feels like: {feels_like}°C)")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        print(f"Condition: {description.capitalize()}")
        print("-" * 50)

def main():
    """Main program"""
    print("\nWelcome to Weather Forecast App!")
    
    # Get city from user
    city = input("\nEnter city name: ").strip()
    
    if not city:
        print("City name cannot be empty!")
        return
    
    # Get coordinates
    print(f"\nSearching for {city}...")
    lat, lon = get_city_coordinates(city)
    
    if lat is None:
        return
    
    # Get weather data
    print("Fetching weather data...")
    weather_data = get_weather(lat, lon)
    
    if weather_data is None:
        return
    
    # Display results
    display_weather(weather_data)
    print("\nThank you for using Weather Forecast App!\n")

# Run the program
if __name__ == "__main__":
    main()