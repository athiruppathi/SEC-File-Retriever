from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time 
import requests
import os 
import tkinter as tk
from tkinter import filedialog
import urllib.request
from bs4 import BeautifulSoup
import sqlite3 

# Set Up Database
conn = sqlite3.connect('master.db')
c = conn.cursor()

c.execute(''' CREATE TABLE IF NOT EXISTS main(
    file_download_path text
    chromedriver_path text
)''')


def get_download_path():
    root = tk.Tk()
    downloadPath = filedialog.askdirectory()
    root.withdraw()
    c.execute('''INSERT INTO main (file_download_path) VALUES (?)''', (downloadPath,))
    return downloadPath

def get_driver_path():
    root = tk.Tk()
    driverPath = filedialog.askopenfilename
    c.execute(''' INSERT INTO main (chromedriver_path) VALUES (?)''', (driverPath,))
    root.withdraw
    return driverPath

# Set Driver Options
c.execute('''SELECT * FROM main WHERE chromedriver_path IS NULL ''')
if c.fetchall() == NULL:
    print('Select the chromedriver executable from your directory')
    time.sleep(4)
    get_driver_path()


# User Input
userTicker = input('Enter company ticker symbol: ').upper()
userType = input('Enter filing type: ').upper()
userNum = int(input('How many would you like to download? '))

c.execute('SELECT file_download_path FROM main')
if c.fetchall() != True:
    print('Specify the desired file location')
    time.sleep(4)
    get_download_path()

# SEC Search Bar and driver settings
options = Options()
options.headless = True
c.execute('SELECT chromedriver_path FROM main')
driverPath = c.fetchall()
#driverPath = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(driverPath,chrome_options=options)
driver.get('https://www.sec.gov/edgar/searchedgar/companysearch.html')
search = driver.find_element_by_id('company')
search.send_keys(userTicker)
search.send_keys(Keys.RETURN)


# File type search bar
fileType = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.ID, 'type'))
)
fileType.send_keys(userType)
fileType.send_keys(Keys.RETURN)


# Click each document button 
docsXPATHList = []
for i in range(2,userNum+2):
    addString = str(i)
    xpathString = f'/html/body/div[4]/div[4]/table/tbody/tr[{i}]/td[2]/a[1]'
    docsXPATHList.append(xpathString)

time.sleep(1)

try:
    downloadList = []
    for doc in docsXPATHList:
        parentWindow = driver.current_window_handle # sets current tab as parent window
        docButton = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH,doc))
        )
        docButton.click()
        print('clicked doc button')
        driver.implicitly_wait(5)
        time.sleep(3)

        # Scrape current html to see if the form is in iXBRL format
        formURL = driver.current_url
        formPage = requests.get(formURL)
        soup = BeautifulSoup(formPage.content,'html.parser')
        table = soup.find("span").text

        if table == 'iXBRL':
            print('in if')
            form= WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'))
                )
            form.click()
            print('form is clicked')
            driver.implicitly_wait(5)
            menuDropDown= WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-dropdown-link"]/i'))
            )
            menuDropDown.click()
            print('menu drop down is clicked')
            driver.implicitly_wait(5)
            openHTML= WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID,'form-information-html'))
            )
            openHTML.click()
            driver.implicitly_wait(5)
            print('open html is clicked')

            childWindows = driver.window_handles
            for w in childWindows:
                if w != parentWindow:
                    driver.switch_to.window(w)
            print(driver.current_url)
            time.sleep(1.5)
            downloadList.append(driver.current_url)  
            time.sleep(1.5)  
            
            driver.switch_to.window(parentWindow)
        
            time.sleep(1.5)  
            driver.back()
        
            time.sleep(1.5)  
            driver.back()
            time.sleep(1.5)  
        
            print(downloadList)

        else:
            print('in else')
            form = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'))
            )
            form.click()
            print('else form clicked')
            driver.implicitly_wait(3)
            time.sleep(1.5)
            downloadList.append(driver.current_url)
            time.sleep(1.5)
            driver.back()
            time.sleep(1.5)
            driver.back()
            time.sleep(1.5)
            #driver.switch_to_window(parentWindow)
            print(downloadList)
except: 
    driver.close()
finally:
    for i in downloadList:
        #print(i)
        c.execute('SELECT file_download_path FROM main')
        downloadPath = c.fetchall()
        index = downloadList.index(i)
        fileIndex = str(index + 1)
        print(downloadPath)
        pathAddition = r"\{} {} {}.html".format(userTicker, userType, fileIndex)
        dynamicPath = downloadPath + pathAddition
        urllib.request.urlretrieve(i, dynamicPath)
        #urllib.request.urlretrieve(i,r"C:\Users\arjun\Downloads\{} {} {}.html".format(userTicker, userType, fileIndex))
    driver.close()
    driver.quit()

conn.commit()
conn.close()