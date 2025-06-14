import os
import requests

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=en"
    response = requests.get(url)
    if response.status_code != 200:
        return None, f"API Error: {response.status_code}"
    data = response.json()
    temp_c = data['current']['temp_c']
    condition = data['current']['condition']['text']
    icon_url = "https:" + data['current']['condition']['icon']  # prepend https

    return (temp_c, condition, icon_url), None