from typing import Dict

import httpx

from src.cfg import weather_api_key

def get_weather_data(query: str) -> Dict:
    """
    Function to fetch weather data for the given city name
    Args:
    query: str
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={query}&appid={weather_api_key}"
    response = httpx.get(url)
    
    weather_data = response.json()
    
    #convert temperature to celsius
    weather_data["main"]["temp"] = round(weather_data["main"]["temp"] - 273.15,2)
    weather_data["main"]["feels_like"] = round(weather_data["main"]["feels_like"] - 273.15,2)
    weather_data["main"]["temp_min"] = round(weather_data["main"]["temp_min"] - 273.15,2)
    weather_data["main"]["temp_max"] = round(weather_data["main"]["temp_max"] - 273.15,2)
    
    return weather_data

if __name__ == "__main__":
    response = get_weather_data("finland")
    print(response)