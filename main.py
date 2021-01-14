from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time 
import requests
import os 
import tkinter as tk
import urllib.request

def get_download_path():
    root = tk.Tk()
    root.withdraw()
    #file_path = filedialog.askopenfilename()

def download_page(url):
    '''Saves webpage as a pdf in the user specified download location'''
    r = requests.get(url, allow_redirects=True) 
    fileName = userTicker + userType
    get_download_path()
    open(fileName,'rb').write(r.content)

# User Input
userTicker = input('Enter company ticker symbol: ').upper()
userType = input('Enter filing type: ').upper()
userNum = int(input('How many would you like to download? '))
print('Specify the desired file location')
#downloadPath = get_download_path

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

#try:
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

print(docsXPATHList, '\n')

downloadList = []
for doc in docsXPATHList:
    parentWindow = driver.current_window_handle
    docButton = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.XPATH,doc))
    )
    docButton.click()
    print('clicked doc button')
    driver.implicitly_wait(5)
    if driver.find_elements_by_xpath('//*[contains(text(), "iXBRL")]'):
    #if driver.find_elements_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/span'):
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

        downloadList.append(driver.current_url)      
        driver.switch_to.window(parentWindow)
        driver.back()
        driver.back()
    else:
        print('in else')
        form = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a'))
        )
        form.click()
        driver.implicitly_wait(5)
        downloadList.append(driver.current_url)
        driver.implicitly_wait(5)
        driver.back()
        driver.back()
        #driver.switch_to_window(parentWindow)
         
print(downloadList)

for i in downloadList:
    #print(i)
    index = downloadList.index(i)
    fileIndex = str(index + 1)
    urllib.request.urlretrieve(i,r"C:\Users\arjun\Downloads\{} {} {}.html".format(userTicker, userType, fileIndex))