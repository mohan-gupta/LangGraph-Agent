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
    
    return response.json()

if __name__ == "__main__":
    response = get_weather_data("finland")
    print(response)