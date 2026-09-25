import os
import datetime
import requests
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from logger_config import logger

load_dotenv()

city_list = [
    'Kolkata', 'Delhi', 'Mumbai', 'Bengaluru',
    'Pune', 'Surat', 'Chennai', 'Ahmedabad',
    'Hyderabad', 'Jaipur'
]

weather_variables = [
    'temperature_2m', 'apparent_temperature',
    'relative_humidity_2m', 'precipitation', 'pressure_msl',
    'cloud_cover', 'wind_speed_10m',
    'wind_direction_10m', 'weather_code'
]

weather_variables_string = ",".join(weather_variables)

start_date = datetime.date.today() - datetime.timedelta(days=1)

geocoding_base_url = os.getenv("GEOCODING_BASE_URL")
historical_weather_data_base_url = os.getenv("HISTORICAL_WEATHER_BASE_URL")


def get_weather_data():

    weather_data_list = []
    city_metadata = []

    for city_id, city in enumerate(city_list, start=1):

        try:
            # Geocoding
            geo_response = requests.get(
                geocoding_base_url,
                params={
                    "name": city.strip(),
                    "count": 1,
                    "countryCode": "IN"
                },
                timeout=20
            )

            geo_response.raise_for_status()

            geo_json = geo_response.json()

            if geo_json.get("results") is None:
                raise ValueError(f"No Geocoding result Found!")

            geo_data = geo_json["results"][0]

            city_metadata.append({
                "city_id": city_id,
                "city_name": geo_data["name"],
                "latitude": geo_data["latitude"],
                "longitude": geo_data["longitude"],
                "country_code": geo_data["country_code"],
                "timezone": geo_data["timezone"]
            })

            # Historical weather
            weather_response = requests.get(
                historical_weather_data_base_url,
                params={
                    "latitude": geo_data["latitude"],
                    "longitude": geo_data["longitude"],
                    "start_date": start_date,
                    "end_date": start_date,
                    "hourly": weather_variables_string,
                    "timezone": geo_data["timezone"]
                },
                timeout=20
            )

            weather_response.raise_for_status()

            if weather_response.json().get('hourly') is None:
                raise ValueError("There is no Weather Data Available!")

            weather_data = weather_response.json()["hourly"]

            weather_data_df = pd.DataFrame(weather_data)

            # Add city ID
            weather_data_df["city_id"] = city_id

            weather_data_list.append(weather_data_df)

            logger.info(f"Successfully extracted weather data for {city}")

        except Exception as e:
            logger.error(
                f"Error during extraction for {city}: {e}"
            )
            return None 

    # Combine all cities
    final_df = pd.concat(
        weather_data_list,
        ignore_index=True
    )

    # City dimension
    dim_city = pd.DataFrame(city_metadata)

    # Create raw directory
    raw_files_input_path = Path.cwd() / "dataset" / "raw"
    raw_files_input_path.mkdir(parents=True, exist_ok=True)

    # Save files
    dim_city.to_csv(
        raw_files_input_path / "dim_city.csv",
        index=False
    )

    final_df.to_csv(
        raw_files_input_path / f"historical_weather_data_{start_date}.csv",
        index=False
    )

    return final_df