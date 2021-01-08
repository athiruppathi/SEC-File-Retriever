from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time 
from lxml import html
import requests
import pdfkit
import os 

def get_download_path():
    pass

def url_to_pdf(url):
    'Saves webpage as a pdf in the user specified download location'
    r = requests.get(url, allow_redirects=True) 
    fileName = userTicker + userType
    get_download_path()
    open(fileName,'rb').write(r.content)

# User Input
userTicker = input('Enter company ticker symbol: ').upper()
userType = input('Enter filing type: ').upper()
userNum = input('How many would you like to download? ')

# SEC Search Bar and driver settings
#chrome_options = Options()
#chrome_options.add_argument("--headless")
path = r"C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(path,options=chrome_options)
driver = webdriver.Chrome(path)
driver.get('https://www.sec.gov/edgar/searchedgar/companysearch.html')
search = driver.find_element_by_id('company')
search.send_keys(userTicker)
search.send_keys(Keys.RETURN)

try:
    # File type search bar
    type = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'type'))
    )
    type.send_keys(userType)
    type.send_keys(Keys.RETURN)

    # Click each document button 
    # docButton= WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.ID, 'documentsbutton'))
    # )
    #docButton.click()  


    docsXPATHList = []
    print('asldk')
    # for i in range(2,userNum+2):
    #     print('in loop')
        # addString = str(i)
        # xpathString = f'/html/body/div[4]/div[4]/table/tbody/tr[{addString}]/td[2]/a[1]'
        # docElement = driver.find_element_by_xpath(xpathString)
        # docsXPATHList.append(docElement)


    #for doc in docsXPATHList:
    docButton = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.ID, 'documentsbutton'))
    )
    docButton.click()
    form= WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'))
    )
    form.click()

    specialDocHeader = driver.find_element_by_xpath('/html/body/nav')
    if specialDocHeader.is_displayed():
        menuDropDown= WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-dropdown-link"]/i'))
        )
        menuDropDown.click()
        openHTML= WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,'form-information-html'))
        )
        openHTML.click()
    
        url_to_pdf(driver.current_url)

    else:
        url_to_pdf(driver.current_url)
         



    # form= WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'))
    # )
    # form.click()

    # specialDocHeader = driver.find_element_by_xpath('/html/body/nav')
    
    # if specialDocHeader.is_displayed():

    #     menuDropDown= WebDriverWait(driver, 5).until(
    #         EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-dropdown-link"]/i'))
    #     )
        
    #     menuDropDown.click()
    #     openHTML= WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.ID,'form-information-html'))
    #     )
    #     openHTML.click()

    # else:
    #     pass

except:
    driver.quit()

finally:
    #pdfkit.from_url(driver.current_url, 'out.pdf')
    pass