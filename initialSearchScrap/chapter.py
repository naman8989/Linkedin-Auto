import requests
import json
import time
import pygetwindow
import pyautogui
from pywinauto import Application
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait


def run(driver):
    print("Starting function in initialSearchScrap.chapter")
    try:
        # all windows
        windows = driver.window_handles
        # change driver to window 1
        driver.switch_to.window(windows[0])

        # open new window
        driver.execute_script(f"window.open('https://www.linkedin.com/')")
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("page is loaded please redirect to search page and adjust your setting")
        time.sleep(2)

        # all windows
        windows = driver.window_handles
        # change driver to window 1
        driver.switch_to.window(windows[1])

        # get the chrome window pointer
        win = pygetwindow.getWindowsWithTitle('Chrome')
        pos = None
        for w in range(len(win)): 
            if win[w].title[:6] == driver.title[:6]:
                pos = w
                break
        app = Application().connect(title=win[pos].title)


        print("----------------------Enter the feds-----------------")
        linkedinLocation = input("Enter the location of search - ")
        domainName = input("Enter the domain Name - ")
        
        # using mouse to enter the domainName
            # click on search
        time.sleep(2)
        ele = driver.find_element(By.CLASS_NAME,"search-global-typeahead__typeahead")
        locat = ele.location
        app[win[pos].title].set_focus()
        pyautogui.moveTo(int(win[pos].topleft[0])+int(locat['x'])+100 , int(win[pos].topleft[1])+int(locat['y'])+200)
        pyautogui.click()
        print("click on textarea .......")

            # filling the search area
        time.sleep(2)
        script = f"""
            document.getElementsByClassName("search-global-typeahead__input search-global-typeahead__input--ellipsis")[0].value = "{domainName}"
        """
        driver.execute_script(script)

            # press enter to search
        time.sleep(1)
        pyautogui.press("enter")
        app[win[pos].title].set_focus()
        pyautogui.moveTo(int(win[pos].topleft[0])+int(locat['x'])+100 , int(win[pos].topleft[1])+int(locat['y'])+400)
        print("press enter to search .....")

        
        # search and click on people
        time.sleep(5)
        script="""
            arr = document.getElementsByClassName("search-reusables__filter-list")[0].children
            arr = Array.from(arr)
            arr.forEach((ele)=>{if(ele.children[0].innerText=='People'){ ele.children[0].click() }})
        """
        driver.execute_script(script)
        print("search and click on people .....")

        # click on active hiring
        time.sleep(4)
        script = """
            function sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }
            async function setup(){
                arr = document.getElementsByClassName("search-reusables__filter-list")[0].children
                arr = Array.from(arr)
                for(var i=0; i<arr.length; i++){
                    try{
                        if (arr[i].children[0].children[1].innerText == 'Actively hiring'){
                            arr[i].children[0].children[1].children[0].click()
                            await sleep(1000)
                            temp = arr[i].children[0].children[0].children[0].children[0].children[1].children[0].children[0].children[1].children[1].children
                            temp = Array.from(temp)
                            for(var j=0; j<temp.length; j++){
                                try{
                                    if (temp[j].children[1].children[0].children[0].innerText == 'Any job title'){
                                        temp[j].children[0].click()
                                    }
                                    await sleep(2000)
                                    temp[0].parentElement.parentElement.parentElement.children[3].children[1].click()
                                    break
                                }catch(err){
                                }
                            }
                            break
                        }
                    }catch(err){
                    }
                }
            }
            setup()
        """
        driver.execute_script(script)
        print("clicking on active hiring .....")


        if not(linkedinLocation == "any" or linkedinLocation == "Any"):

            # setup location
                # settle up the data
            time.sleep(7)
            script=("""
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }
                async function locationSetup() {
                    arr = document.getElementsByClassName("search-reusables__filter-list")[0].children
                    arr = Array.from(arr)
                   for (var i = 0; i < arr.length; i++) {
                        try {
                            if (arr[i].children[0].children[1].innerText == 'Locations') {
                                arr[i].children[0].children[1].children[0].click();
                                await sleep(1000);

                                """+

                                f"arr[i].children[0].children[0].children[0].children[0].children[1].children[0].children[0].children[1].children[0].children[0].children[0].value = '{linkedinLocation}';"+
                            """
                                break;
                            }
                        } catch (err) {
                            console.error(err);
                        }
                    }
                }
                locationSetup();
            """)
            driver.execute_script(script)
            print("clicking on location and setting the user location ....")

            # click on the search
            time.sleep(2)
            ele = driver.find_element(By.ID,"searchFilter_geoUrn")
            locat = ele.location
            app[win[pos].title].set_focus()
            pyautogui.moveTo(int(win[pos].topleft[0])+int(locat['x'])+150 , int(win[pos].topleft[1])+int(locat['y'])+285)
            pyautogui.click()
            time.sleep(1)
            pyautogui.press("space")
            print("Enter location .....")

            # click on the cell
            time.sleep(2)
            pyautogui.moveTo(int(win[pos].topleft[0])+int(locat['x'])+150 , int(win[pos].topleft[1])+int(locat['y'])+335)
            pyautogui.click()
            print("Select location ......")

            # click on search result
            time.sleep(2)
            script="""
                arr = document.getElementsByClassName("search-reusables__filter-list")[0].children
                arr = Array.from(arr)
                for (var i = 0; i < arr.length; i++) {
                    try {
                        if (arr[i].children[0].children[1].innerText == 'Locations'){
                            arr[i].children[0].children[0].children[0].children[0].children[1].children[0].children[0].children[3].children[1].click()
                            break
                        }
                    } catch (err) {
                        console.error(err);
                    }
                }
            """
            driver.execute_script(script)


       
        
        
        
        tem = input("input 'f' to bypass else input a number to till the page you want to run the code \n Waiting for your response >>> ")
        if tem == 'f':
            raise Exception("code is bypassed by the user !!")


        
        # looping till the end page
        tem = int(tem)
        while int(tem):
            tem -= 1
            script = """
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }
                isFetching = false
                async function fetch(){
                    if (isFetching) return; // Stop if already running
                    isFetching = true;

                    t=document.getElementsByClassName("artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view artdeco-pagination__button artdeco-pagination__button--next")[0]
                    window.scrollTo(0, document.body.scrollHeight - (24 *10) - (32*10) );
                    temp = document.getElementsByClassName("reusable-search__entity-result-list list-style-none")
                    await sleep(3000)
                    if (temp[0].children != 'undefine'){
                        arr = Array.from(temp[0].children)
                    }else{
                        arr = Array.from(temp[1].children)
                    }
                    ret = []
                    arr.forEach(ele=>{
                        try {
                            te = ele.children[0].children[0].children[0].children[1].children[0].children[0].children[0].children[0].children[0].children[0].getAttribute("href")
                            if( !( te.includes("[") || te.includes("]") || te.includes("results") ) ){
                                console.log(te)
                                ret.push(te)
                            }
                            else{
                                console.log("error in - ",te)
                            }
                        } catch (error) { 
                        } 
                    })
                    localStorage.setItem("alllinks",JSON.stringify(ret))
 
                }
                fetch()
            """
            driver.execute_script(script)
            print("scraped all the links ")

            # return the data from localstorage
            time.sleep(5)
            script = """
                return localStorage.getItem("alllinks")
            """
            arr = driver.execute_script(script)
            print("got the links")

            # data adjustment
            temp = json.loads(arr)
            dataFed = ""
            for i in range(len(temp)):
                dataFed += f"{domainName} , " + temp[i] + f", {linkedinLocation}" + "|"
            dataFed = dataFed[:len(dataFed)-1]
            print("data adjusted")
            print(temp)

            # push to database
            if len(temp) != 0:
                requests.get(f"http://127.0.0.1:5000/pushDatatoTable?totalInp={len(temp)}&useTable=profpersons&location=field,personlink,location&data={dataFed}")
            print("data send to database api")

            # load next page
            script="""
                document.getElementsByClassName("artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view artdeco-pagination__button artdeco-pagination__button--next")[0].click()
            """
            driver.execute_script(script)
            print("next page clicked")

            # wait to load next page
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.getElementsByClassName('reusable-search__entity-result-list list-style-none')[0] ") != 'undefined'
            )
            print(f"next page loaded  starting tem - {tem+1}")
            time.sleep(2)

        
        
        print("in the end of initialSearchScrap.chapter ",linkedinLocation," ",domainName)

    except Exception as e:
        print("some thing came up ",e)
        

    # close window
    driver.close()
    # driver point back to window 1
    driver.switch_to.window(windows[0])

    