import logging
import sys

from scraper import Scrapper
from database import Database

import pandas as pd

logging.basicConfig(filename="scraper.log",
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

scraper = Scrapper("https://www.daraz.pk/", "laptop")
logger.info("Scrapping started")

# logger.info("Connecting to database")
database = Database("talha", "izmeh", "mydatabase")


scraper.scrap_product(pages=1)
dataframe = scraper.to_dataframe()

scraper.show_dataframe()
scraper.show_dataframe_info()

database.insert_data(dataframe)
database.show_database()
