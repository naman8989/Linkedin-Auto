from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import requests


# send data to database
def sendDataToDatabase(data):
    try:
        dataSlice = data.split("||")
        for com in dataSlice:
            if len(com) != 0:
                tem = com.split("|")
                try:
                    requests.get(f"http://127.0.0.1:5000/companyData?cn={tem[0]}&cl={tem[1]}&cu={tem[2]}")
                except Exception as err:
                    print("error while send data to database")
                    print(err)
    except:
        print("got no exprience data")

# set url 
with open(f"{os.getcwd()}\scratchCom\scratchScript.js", "r") as file:
    script = file.read()

driver = webdriver.Chrome()
url = "https://www.linkedin.com/"
# set url and driver
driver.get(url)
# Wait for the page to fully load by checking document.readyState
WebDriverWait(driver, 7).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
) 

input()

print("-----starting-------")
urlFile = open(f"{os.getcwd()}/scratchCom/urls.txt", "r") 
url = urlFile.readline()  
while url != '':
    # open new tab
    url = url.replace("\n","")
    print(url)
    driver.execute_script(f"window.open('{url}');")
    # all windows
    windows = driver.window_handles
    # change driver to window 1
    driver.switch_to.window(windows[1])
    # wait 10s
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    ) 
    time.sleep(3)
    # Run JavaScript
    driver.execute_script(script)
    print('script injected')
    time.sleep(2)
    data = driver.execute_script("return localStorage.getItem('companyData')")
    sendDataToDatabase(data)
    # sleep
    time.sleep(1)
    # close cur tab
    driver.close()
    # switch back 0 tab
    driver.switch_to.window(windows[0])
    url = urlFile.readline()  




input()
driver.close()