import lxml as lx 
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time 


# userTicker = input('Enter company ticker symbol: ').upper()
# userType = input('Enter filing type: ').upper()
# userNum = input('How many would you like to download? ')


path = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get('https://www.sec.gov/edgar/searchedgar/companysearch.html')
search = driver.find_element_by_id('company')
#search.send_keys(userTicker)
search.send_keys('AMZN')
search.send_keys(Keys.RETURN)

try:
    type = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'type'))
    )
    #type.send_keys(userType)
    type.send_keys('10-Q')
    type.send_keys(Keys.RETURN)


    docButton= WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'documentsbutton'))
    )
    docButton.click()

    form= WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'))
    )
    form.click()
except:
    driver.quit()

