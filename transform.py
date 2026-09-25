import pandas as pd
from pathlib import Path
from logger_config import logger
import datetime
def __validate_weather_data(weather_data_df):
    # Check for Rquired Columns in dataframe
    require_columns = ['time',
    'temperature_2m',
    'apparent_temperature',
    'relative_humidity_2m',
    'precipitation', 
    'pressure_msl',
    'cloud_cover', 
    'wind_speed_10m', 
    'wind_direction_10m', 
    'weather_code' , 'city_id']

    missing_columns = set(require_columns) - set(weather_data_df.columns.to_list())

    extra_columns = set(weather_data_df.columns.to_list()) - set(require_columns)
    
    if len(missing_columns) >= 1:
        logger.error(f"There is some Missing Columns in the the Dataframe")
        return False
    if len(extra_columns) >= 1 :
        logger.error("There is Some Extra Columns in the Weather Dataframe")
        return False
    
    return True 
    
def clean_weather_data(weather_data_df):
    if __validate_weather_data(weather_data_df) :
        # Convert Time Column into Proper Timestamp
        weather_data_df['time'] = pd.to_datetime(weather_data_df['time'] , errors='coerce')
        # Convert Other Columns into Numerical DataType
        for col in weather_data_df.select_dtypes(include = ['int64' , 'float64']).columns.to_list():
            weather_data_df[col] =pd.to_numeric(weather_data_df[col])
        # Rename Columns from time to timestamp
        weather_data_df = weather_data_df.rename(columns = {'time':'timestamp'})    
        # Remove Duplicates Records  from Dataframe
        weather_data_df = weather_data_df.drop_duplicates(keep = 'first')  
        # Remove Null Records 
        weather_data_df = weather_data_df.dropna()
        if len(weather_data_df) == 240 :
            # Create Processed & Clean Files Directory
            start_date = datetime.date.today() - datetime.timedelta(days = 1)
            processed_files_folder_path = Path.cwd() / 'dataset' / 'processed'
            processed_files_folder_path.mkdir(parents = True , exist_ok = True)
            # Save the Cleaned Dataframe into CSV File
            weather_data_df.to_csv(processed_files_folder_path / f'cleaned_weather_data_{start_date}.csv' , index = False) 
            logger.info(f"Cleaned Weather Dataframe is Saved into CSV File at {processed_files_folder_path / f'cleaned_weather_data_{start_date}.csv'}")
            return weather_data_df
        else:
            logger.warning("Total Number of Records is not Matching in the Dataframe")
            return None 
    else:
        return None  


