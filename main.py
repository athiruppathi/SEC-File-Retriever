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

while True:

    c.execute(''' CREATE TABLE IF NOT EXISTS main(
        file_download_path TEXT,
        chromedriver_path TEXT
    )''')

    def set_driver_path():
        root = tk.Tk()
        driverPath = filedialog.askopenfilename()
        print(driverPath)
        c.execute('INSERT INTO main (chromedriver_path) VALUES (?)', (driverPath,))
        print(c.fetchall())
        conn.commit()
        root.withdraw

    def get_driver_path():
        c.execute('SELECT chromedriver_path FROM main WHERE chromedriver_path IS NOT NULL')
        result = c.fetchall()[0][0]
        print(result)
        return result
        
    def set_download_path():
        root = tk.Tk()
        downloadPath = filedialog.askdirectory()
        print(downloadPath)
        c.execute('''INSERT INTO main (file_download_path) VALUES (?)''', (downloadPath,))
        conn.commit()
        root.withdraw()

    def get_download_path():
        c.execute('SELECT file_download_path FROM main WHERE file_download_path IS NOT NULL')
        result = c.fetchall()[0][0]
        return result

    def is_empty_list(l):
        if len(l) == 0:
            return True
        else:
            pass

    # Set Driver Options if it's first time setup
    c.execute('SELECT chromedriver_path FROM main')
    if is_empty_list(c.fetchall()) :
        print('Set your chromedriver download path. If chromedriver is not downloaded, download it here: \n\
            https://chromedriver.chromium.org/downloads  and re-run the program')
        time.sleep(3)
        set_driver_path()

    # User Input
    userTicker = input('Enter company ticker symbol: ').upper()
    userType = input('Enter filing type: ').upper()
    userNum = int(input('How many would you like to download? '))

    # Set Download Path for first time 
    c.execute('SELECT file_download_path FROM main')
    #print(len(c.fetchall()))
    if len(c.fetchall()) < 2: 
        print('Set your file download location (this will be the default location)')
        time.sleep(3)
        set_download_path()

    # SEC Search Bar Entry
    options = Options()
    options.headless = True
    driverPath = get_driver_path()
    driver = webdriver.Chrome(driverPath,options=options)
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
            driver.implicitly_wait(5)
            time.sleep(3)

            # Scrape current html to see if the form is in iXBRL format
            formURL = driver.current_url
            formPage = requests.get(formURL)
            soup = BeautifulSoup(formPage.content,'html.parser')
            table = soup.find("span").text

            if table == 'iXBRL':
                form= WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'))
                    )
                form.click()

                driver.implicitly_wait(5)
                menuDropDown= WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-dropdown-link"]/i'))
                )
                menuDropDown.click()

                driver.implicitly_wait(5)
                openHTML= WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID,'form-information-html'))
                )
                openHTML.click()
                driver.implicitly_wait(5)

                childWindows = driver.window_handles
                for w in childWindows:
                    if w != parentWindow:
                        driver.switch_to.window(w)

                time.sleep(1.5)
                downloadList.append(driver.current_url)  
                time.sleep(1.5)  
                
                driver.switch_to.window(parentWindow)
            
                time.sleep(1.5)  
                driver.back()
            
                time.sleep(1.5)  
                driver.back()
                time.sleep(1.5)  
            
            else:

                form = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'))
                )
                form.click()

                driver.implicitly_wait(3)
                time.sleep(1.5)
                downloadList.append(driver.current_url)
                time.sleep(1.5)
                driver.back()
                time.sleep(1.5)
                driver.back()
                time.sleep(1.5)

    except: 
        print('Error in program.')

    finally:
        downloadPath = get_download_path()
        for i in downloadList:
            index = downloadList.index(i)
            fileIndex = str(index + 1)
            pathAddition = r"\{} {} {}.html".format(userTicker, userType, fileIndex)
            dynamicPath = downloadPath + pathAddition
            urllib.request.urlretrieve(i, dynamicPath)
        driver.close()
        driver.quit()

    c.execute('DELETE FROM main WHERE rowid NOT IN (SELECT min(rowid) FROM main GROUP BY file_download_path, chromedriver_path)')

    while True:
        print('Done')
        answer = str(input('Run again? (y/n): ')).lower()
        if answer in ('y','n'):
            break
        print('invalid input')
    if answer == 'y':
        continue
    else:
        print('Goodbye')
        break
conn.commit()
conn.close()