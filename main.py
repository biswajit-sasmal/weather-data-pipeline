import importlib 
import extract 
import transform
import load
importlib.reload(extract)
importlib.reload(transform)
importlib.reload(load)
from logger_config import logger
def main():
    logger.info("Pipeline Started")
    try:
        weather_raw_data = extract.get_weather_data()
        if weather_raw_data is None :
            logger.info("Pipeline Stop")
            return None
        clean_data =transform.clean_weather_data(weather_raw_data)
        if clean_data is None :
            logger.info("Pipeline Stop")
            return None
        load_data = load.load_weather_data(clean_data)
        if load_data is None:
            logger.info("Pipeline Stop")
            return None
        logger.info("Pipeline Completed Successfully!")

    except Exception:
        logger.exception("Unexpected Error Occured Pipeline Stopped")    

if __name__ == "__main__":
    main()
      

    