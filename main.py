import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


os.environ['PATH'] += r"D:\Projects\python\selenium_drivers"
driver=webdriver.Chrome()
driver.get("http://www.amis.pk/Daily%20Market%20Changes.aspx")
element=driver.find_element(by=By.ID,value="ctl00_cphPage_GridView1")

driver.implicitly_wait(30)
# Split the text into rows
rows = element.text.split("\n")

# Get the column names from the first row
column_names = rows[0].split()

# Initialize an empty list to store the data
data = []

# Iterate over the remaining rows
for row in rows[1:]:
    # Split the row by spaces to get the values
    values = row.split()
    # Create a dictionary for the row
    row_dict = dict(zip(column_names, values))
    # Add the dictionary to the data list
    data.append(row_dict)

print(data)
# data now contains the list of dictionaries
