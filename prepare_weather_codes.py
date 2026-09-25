import pandas as pd 
from pathlib import Path

def clean_data():
    weather_code_json_file_path = Path.cwd() / "dataset" / "descriptions.json"

    weather_code_df = pd.read_json(weather_code_json_file_path)

    transpose_weather_df =  weather_code_df.transpose()

    transpose_weather_df['weather_description'] = transpose_weather_df['day'].apply(lambda x: x['description'])

    transpose_weather_df = transpose_weather_df.reset_index()

    transpose_weather_df = transpose_weather_df.rename(columns={"index": "weather_code"})

    transpose_weather_df = transpose_weather_df[['weather_code' , 'weather_description']]

    transpose_weather_df.to_csv(Path.cwd() / "dataset" / "raw" / "dim_weather.csv" , index = False)

    return transpose_weather_df