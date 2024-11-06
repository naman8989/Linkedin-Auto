import importlib
import index
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait



driver = webdriver.Chrome()
url = "https://www.linkedin.com/"
# set url and driver
driver.get(url)
# Wait for the page to fully load by checking document.readyState
WebDriverWait(driver, 7).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
) 

input("Driver started \n Press any key to continue ...............\n") 

temp = ""
while temp != 'f':
    try:
        importlib.reload(index)
        print("reloaded index.py")
        print("poke the run() function in index.py")
        index.run(driver)
    except Exception as e:
        print("in the exception of main.py ",e)
        # driver.get(url)
        # Wait for the page to fully load by checking document.readyState
        # WebDriverWait(driver, 7).until(
        #     lambda d: d.execute_script("return document.readyState") == "complete"
        # ) 
    
    temp = input("Press !('f') key to continue looping.. > ")
    