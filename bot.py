import logging
import sys

from scraper import Scrapper
from database import Database

def bot():
    # Create a custom logger
    logging.basicConfig(filename="scraping_bot.log",
                        format='%(asctime)s %(message)s',
                        filemode='w',
                        level=logging.INFO)

    logger = logging.getLogger()

    # Create a stream handler and set its level to INFO
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)

    # Create a formatter for the stream handler
    formatter = logging.Formatter('%(asctime)s %(message)s')

    # Set the formatter for the stream handler
    stream_handler.setFormatter(formatter)

    # Add the stream handler to the logger
    logger.addHandler(stream_handler)

    logger.info("Collecting product information")
    scraper = Scrapper("https://www.daraz.pk/", "laptop")



    logger.info("Product scrapping started")
    scraper.scrap_product(pages=10)

    logger.info("Converting to dataframe")
    dataframe = scraper.to_dataframe()

    scraper.show_dataframe()
    scraper.show_dataframe_info()
    
    
    logger.info("Collecting database credentials")
    database = Database("talha", "izmeh", "mydatabase")

    logger.info("Inserting data into database")
    database.insert_data(dataframe)


    database.show_database()
