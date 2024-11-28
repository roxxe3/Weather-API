from flask import Flask, jsonify
import requests
import json
import redis
import os
from dotenv import load_dotenv

load_dotenv()

def parse_weather_data(data):
    """
    Parses weather data to extract temperature information for each day.

    Args:
        data (dict): A dictionary containing weather data with a 'days' key. 
                     Each item in 'days' is expected to be a dictionary with 
                     'datetime' and 'temp' keys.

    Returns:
        dict: A dictionary where the keys are dates (as strings) and the values 
              are the corresponding temperatures.
    """
    new_dict = {}
    for day in data['days']:
        current_day = day["datetime"]
        temp = day['temp']
        new_dict[current_day] = temp
    return new_dict


app = Flask(__name__)
api_key = os.getenv("api_key")
if api_key is None:
    raise ValueError("API key not found. Please set the 'api_key' environment variable.")

r = redis.Redis(host='localhost', port=6379)

def get_weather(city):

    """
    Fetches weather data for a given city from the Visual Crossing Weather API, 
    caches the data in Redis, and returns the parsed weather data.

    Args:
        city (str): The name of the city for which to fetch the weather data.

    Returns:
        dict: Parsed weather data if the API request is successful.
        str: "No data" if the API request fails.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the API request.
    """

    weather_api = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days&key={api_key}&contentType=json"
    key = f"location:{city}"
    try:
        response = requests.get(weather_api)
        response.raise_for_status()  # Raise an error for HTTP codes >= 400
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}
    weather_data = parse_weather_data(data)
    dict_data = json.dumps(weather_data)
    r.set(key, dict_data, ex=12 * 60 * 60)
    print("Data fetched from API")
    return weather_data

def get_cache(city):

    """
    Retrieve weather data for a given city from the cache.

    This function attempts to fetch weather data for the specified city from a Redis cache.
    If the data is not available in the cache or if there is a connection error, it falls back
    to fetching the data from the weather API.

    Args:
        city (str): The name of the city for which to retrieve weather data.

    Returns:
        dict or str: The weather data for the specified city as a dictionary if successful,
                     or an error message string if the Redis server is not available.
    """

    key = f"location:{city}"
    try:
        data = r.get(key)
    except redis.exceptions.ConnectionError:
        return "Redis server is not available"
    if data is None:
        return get_weather(city)
    else:
        decoded_data = data.decode("utf-8")
        parsed_data = json.loads(decoded_data)
        print("Data fetched from cache")
        return parsed_data

@app.route('/weather/<city>')
def get_weather_data(city):
    cache = get_cache(city)
    return jsonify(cache)

if __name__ == '__main__':
    app.run(debug=True)