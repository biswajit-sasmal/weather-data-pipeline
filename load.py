from sqlalchemy import create_engine , text 
from urllib.parse import quote_plus
import os 
from logger_config import logger
import pandas as pd 
import datetime
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_username = os.getenv("DB_USERNAME")
db_password = quote_plus(os.getenv("DB_PASSWORD"))
db_port = os.getenv("DB_PORT")
connection_string = "postgresql://" + db_username + ':' + db_password + '@' + db_host + ':' + db_port + '/' + db_name

engine = create_engine(connection_string)
    
def load_weather_data(clean_weather_df):
    last_date_query = text("select cast(max(timestamp)as date) as last_date from weather.fact_weather_hourly ;")
    for query_attempt in range(3):  # Retry mechanism
        try:
            with engine.connect() as connection1:
                last_date = connection1.execute(last_date_query).scalar()
            break  # If successful, exit the retry loop
        except Exception as e:
            logger.error(f"Error occurred while fetching last date: {e}")
    else:
        logger.error("Failed to fetch last date from database 'fact_weather_hourly' table after 3 attempts.")
        return None

    clean_weather_df['timestamp'] = pd.to_datetime(clean_weather_df['timestamp'] , errors='coerce')

    if clean_weather_df['timestamp'].min() == pd.Timestamp(last_date):
        logger.warning("Duplicate data detected. The minimum timestamp in the new data matches the last timestamp in the database. No new data will be loaded.")
        return None 
    with engine.connect() as connection2:
        for load_attempt in range(3):  # Retry mechanism for loading data
            try:
                clean_weather_df.to_sql('fact_weather_hourly', con=connection2, schema='weather', if_exists='append', index=False)
                logger.info("Data loaded successfully into the database.")
                break  # If successful, exit the retry loop
            except Exception as e:
                logger.error(f"Error occurred while loading data (attempt {load_attempt + 1}): {e}")
        else:
            logger.error("Failed to load data into Database after 3 attempts.")
            return None 

        


