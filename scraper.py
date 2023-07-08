import re
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Scrapper:
    def __init__(self, url: str, product_name: str) -> None:
        self.url = url
        self.product_name = product_name
        self.product_info = {}
        self.dataframe = None

    def scrap_product(self, pages=3) -> None:  
        driver = webdriver.Chrome()
        driver.get(self.url)

        try:
            search_bar = driver.find_element(By.XPATH, '//*[@id="q"]')  # find search bar
            search_bar.send_keys(self.product_name)  # send product name to search bar

            search_btn = driver.find_element(By.XPATH, '//*[@id="topActionHeader"]/div/div[2]/div/div[2]/form/div/div[2]/button')  # find search button
            search_btn.click()
            print("Search button clicked")

            # how many entries are there
            total_prod = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div')
            print("TOTAL Entries Found:", total_prod.text)
            time.sleep(2)
            id_counter = 0  # Counter for ID

            for i in range(pages):  # Iterate through pages
                products = driver.find_elements(By.CLASS_NAME, 'gridItem--Yd0sa')
                print("Products found:", len(products))
                
                for product in products:
                    product_info = product.text
                    name_match = re.search(r'^(.*?)\n', product_info, re.MULTILINE)
                    name = name_match.group(1) if name_match else ""
                    disc_price_match = re.search(r'Rs\. (\d+(?:,\d+)*)', product_info)
                    disc_price = disc_price_match.group(1) if disc_price_match else 0
                    orig_price_match = re.search(r'Rs\. (\d+(?:,\d+)*)-(\d+)%', product_info)
                    orig_price = orig_price_match.group(1) if orig_price_match else 0
                    discount = orig_price_match.group(2) if orig_price_match else "0"
                    rating_match = re.search(r'\((\d+)\)', product_info)
                    rating = rating_match.group(1) if rating_match else 0
                    shipping_match = re.search(r'Free Shipping', product_info)
                    shipping = "Free Shipping" if shipping_match else "No Free Shipping"

                    self.product_info[name] = {
                        'ID': int(id_counter),
                        'Discounted Price': disc_price,
                        'Original Price': orig_price,
                        'Discount(%)': discount + "%" if discount else "0%",
                        'Rating': int(rating),
                        'Shipping': shipping
                    }
                    id_counter += 1  # Increment the ID counter
                    # time.sleep(1)
                    
                next_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[1]/div[3]/div/ul/li[9]/a')
                if next_btn.is_enabled():
                    driver.execute_script("arguments[0].click();", next_btn)
                    print(f'Button is pressed now we are on page: {i+1}')
                    time.sleep(7)  # Wait for the page to load
                else:
                    raise NoSuchElementException("No more pages to load")
            self.product_info = {name: {'Name': name, **data} for name, data in self.product_info.items()}
        except NoSuchElementException as e:
            print("Error occurred during scraping.")
            raise e

    def to_dataframe(self) -> pd.DataFrame:
            self.dataframe = pd.DataFrame.from_dict(self.product_info, orient='index')
            self.dataframe.reset_index(drop=True, inplace=True)  # Remove the first column
            
            # Rename the existing column
            self.dataframe.rename(columns={"ID": "Old_ID"}, inplace=True)
            
            # Insert the new "ID" column at the first position
            self.dataframe.insert(0, "ID", self.dataframe.index)
            
            # Drop the "Old_ID" column
            self.dataframe.drop(columns="Old_ID", inplace=True)
            
            self.dataframe.to_csv('product_info.csv', index=False)  # Exclude index in CSV output
            return self.dataframe
    
    def show_dataframe(self) -> None:    
        print(self.dataframe.head())
        
    def show_dataframe_info(self) -> None:
        print(self.dataframe.info())
