DROP SCHEMA IF EXISTS weather CASCADE;

CREATE SCHEMA weather;

-- Drop fact table first, then dimension table to respect dependencies
DROP TABLE IF EXISTS weather.fact_weather_hourly;
DROP TABLE IF EXISTS weather.dim_city;

CREATE TABLE weather.dim_city (
    city_id INT PRIMARY KEY,
    city_name VARCHAR(30),
    latitude FLOAT,
    longitude FLOAT,
    country_code CHAR(2),
    timezone VARCHAR(20)
);

DROP TABLE IF EXISTS weather.dim_weather;

CREATE TABLE weather.dim_weather
(
weather_code INT PRIMARY KEY,
weather_description VARCHAR(100)    
);

CREATE TABLE weather.fact_weather_hourly (
    timestamp TIMESTAMP,
    temperature_2m DECIMAL(3, 1),
    apparent_temperature DECIMAL(3, 1),
    relative_humidity_2m SMALLINT,
    precipitation DECIMAL(3, 1),
    pressure_msl DECIMAL(5, 1),
    cloud_cover SMALLINT,
    wind_speed_10m DECIMAL(3, 1),
    wind_direction_10m SMALLINT,
    weather_code SMALLINT,
    city_id INT, -- Matched to INT to align with dim_city
    CONSTRAINT fk_city FOREIGN KEY (city_id) REFERENCES weather.dim_city(city_id),
    CONSTRAINT fk_weather FOREIGN KEY (weather_code) REFERENCES weather.dim_weather(weather_code)
);