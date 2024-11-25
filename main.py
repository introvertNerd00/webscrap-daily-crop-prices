import os
import pyodbc
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

os.environ['PATH'] += r"D:\Projects\python\selenium_drivers"

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.amis.pk/Daily%20Market%20Changes.aspx")
element=driver.find_element(by=By.XPATH,value="(//tbody)[1]")

driver.implicitly_wait(30)
# Split the text into rows
rows = element.text.split("\n")

# Initialize an empty list to store the data
data = []

# Iterate over the rows
for row in rows:
    # Split the row by spaces from the right side to get the last three columns
    values = row.rsplit(maxsplit=3)
    # Further split the remaining part to separate the location and item
    location, item = values[0].split(maxsplit=1)
    # Create a dictionary for the row
    row_dict = {
        "Location": location,
        "Item": item,
        "Old Price": values[1],
        "New Price": values[2],
        "Change": values[3]
    }
    # Add the dictionary to the data list
    data.append(row_dict)

print(data)
# data now contains the list of dictionaries

def insert_data_to_mssql(data):
    # Define the connection string using environment variables
    conn_str = (
        # f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        # f"SERVER={os.getenv('DB_SERVER')};"
        # f"DATABASE={os.getenv('DB_NAME')};"
        # f"UID={os.getenv('DB_USER')};"
        # f"PWD={os.getenv('DB_PASSWORD')}"
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-H3O6FTO\\SQLEXPRESS;"
        "DATABASE=AgriTech;"
        "Trusted_Connection=yes;"
    )
    # Establish the connection
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Insert data into the table
    for row in data:
        try:
            print(f"Attempting to convert New Price to float: {row['New Price']}")
            new_price = float(row['New Price'])
            cursor.execute('''
            INSERT INTO crop_prices (city, date, crop_name, price)
            VALUES (?, ?, ?, ?)
            ''', row['Location'], current_date, row['Item'], new_price)
        except ValueError as e:
            print(f"Error converting New Price to float: {e}")
    
    
    # Commit the transaction
    conn.commit()
    # Close the connection
    conn.close()

# Call the function to insert data into MSSQL
insert_data_to_mssql(data)
