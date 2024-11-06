import importlib
import mod
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


tem = True

driver = webdriver.Chrome()
url = "https://www.linkedin.com/"
# set url and driver
driver.get(url)
# Wait for the page to fully load by checking document.readyState
WebDriverWait(driver, 7).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
) 

input("Driver started \n Press any key to continue ...............\n") 

while tem:
    importlib.reload(mod)
    mod.run(driver)
    
    t = input("Press !('f') key to continue looping.. > ")
    if t == "f":
        tem = False
    