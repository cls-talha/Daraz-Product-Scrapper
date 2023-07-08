import mysql.connector as connector
from sqlalchemy import create_engine
import pandas as pd

class Database:
    def __init__(self, username: str, password: str, database: str) -> None:
        self.username = username
        self.password = password
        self.database = database
        try:
            self.my_database = connector.connect(
                host="localhost",
                user=self.username,
                password=self.password,
                database=self.database
            )
            if self.my_database.is_connected():
                print("INFO Connected with database")
        
        except connector.Error as e:
            print("INFO Connection Failed")
            raise ValueError(str(e))

    def insert_data(self, dataframe) :
        try:
            self.cursor = self.my_database.cursor()
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            print("Tables:", tables)
            engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@localhost/{self.database}")
            dataframe.to_sql(name='daraz_records', con=engine, if_exists='replace', index=True)
            self.my_database.commit()
            print("Data inserted successfully!")
            
        except connector.Error as e:
            print("INFO Connection Failed")
            raise ValueError(str(e))
    
    def show_database(self) -> None: 
        self.cursor = self.my_database.cursor()
        query = "SELECT * FROM daraz_records"  # Replace daraz_records with the actual table name
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
            print("\n")
            
    def __del__(self):
        print("INFO Closing database connection")
        self.cursor.close()
        self.my_database.close()
