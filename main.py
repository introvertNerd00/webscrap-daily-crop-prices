import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

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
    # Split the row by spaces from the right side to get the values
    values = row.rsplit(maxsplit=4)
    # Create a dictionary for the row
    row_dict = {
        "Location": values[0],
        "Item": values[1],
        "Old Price": values[2],
        "New Price": values[3],
        "Change": values[4]
    }
    # Add the dictionary to the data list
    data.append(row_dict)

print(data)
# data now contains the list of dictionaries
