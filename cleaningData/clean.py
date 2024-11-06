import requests
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class clean:
    # get all rows
    def getTotalRows(self,table):
        res = requests.get(f"http://127.0.0.1:5000/tableSize?tableName={table}")
        return json.loads(res.content)[0][4]

    # getTotalRows('allcompanydata')

    def getTableData(self,table,offs,nums):
        res = requests.get(f"http://127.0.0.1:5000/getRawRow?table={table}&stRow={offs}&nums={nums}")
        return json.loads(res.content)

    def sendDatatoDatabase(self,conData,orgUrl,storedName):
        if conData == None:
            print("----------Got the none----------")
            url =  f"http://127.0.0.1:5000/pushDatatoTable?totalInp=2&useTable=uncleandata&location=originalUrl|storedCompName&data={orgUrl}|{storedName}"
            print("company not found")
        else:
            
            url =  f"http://127.0.0.1:5000/pushDatatoTable?totalInp=3&useTable=cleandata&location=originalUrl|companyName|newUrl&data={orgUrl}|{conData}"
        
        try:
            ret = requests.get(url)
            return json.loads(ret.content)
        except:
            print("Company already existed")
            return "Company already existed"

    

# read script
with open(f"{os.getcwd()}\cleaningData\cleanScript.js") as file:
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

print("------------starting---------------")
gather = clean()
pos = 324

totalRows = gather.getTotalRows('allcompanydata')
while pos != totalRows-1:
    data = gather.getTableData('allcompanydata',pos,1)
    print(data[0][2],"   | pos - ",pos)
    try:
        driver.execute_script(f"window.open('{data[0][2]}');")
        # all windows
        windows = driver.window_handles
        # change driver to window 1
        driver.switch_to.window(windows[1])
        # wait 10s
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        ) 
        time.sleep(3)
        driver.execute_script(script)
        print('script injected')
        time.sleep(1)
        confirmData = driver.execute_script("return localStorage.getItem('compData')")
        gather.sendDatatoDatabase(confirmData,data[0][2],data[0][0])
        time.sleep(1)
        driver.close()
        driver.switch_to.window(windows[0])
    except:
        print("something wrong with current url")

    
    pos += 1


input()
driver.close()