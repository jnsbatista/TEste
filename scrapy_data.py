from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from retrying import retry #Retrying is an Apache 2.0 licensed general-purpose retrying library, written in Python, to simplify the task of adding retry behavior to just about anything. The simplest use case is retrying a flaky function whenever an Exception occurs until a value is returned.


table = [[],[],[]] # table n x 3

@retry(stop_max_attempt_number=10, wait_fixed=2000)
def login():
  user_pw = "teste"
  # First access to the page
  url = "https://www.montmere.com/test.php"
  driver = webdriver.Firefox(executable_path="./geckodriver.exe")
  driver.get(url)
  
  # Login
  driver.find_element(By.ID,'username').send_keys(user_pw)
  driver.find_element(By.ID,'password').send_keys(user_pw)
  driver.find_element(By.XPATH, "//input[@value='Login']").click()
  
  # Wait 4 seconds to ensure the page will load
  time.sleep(4)
  # Search for lines with content
  rows = driver.find_elements(By.CSS_SELECTOR, 'table.table tr')
  
  if (not rows):
    raise RuntimeError("ERROR!")
  else:
    # For loop in each column of each selected row
    for i in range(1,len(rows)):
      cols = rows[i].find_elements(By.TAG_NAME,"td")
      for g in range(0,len(cols)):
        # Save the data in the table
        table[g].append(cols[g].text)
        
    driver.close()    
    return create_csv()

# Function to create CSV
def create_csv():
  # Make Dataframe with dates of table
  cars_table = pd.DataFrame({'Make' : table[0], 'Model' : table[1], 'Year': table[2]})
  # sort by date
  cars_table = cars_table.sort_values(by=['Year'], ascending=False)
  # Set index
  cars_table = cars_table.set_index('Year', inplace=False)
  # Create CSV
  cars_table.to_csv('cars_table.csv')
  
login()