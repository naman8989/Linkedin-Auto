from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os 
import time
import requests
import json
import Levenshtein


def getUrl(ind):
    try :
        query = f"SELECT * From cleandata LIMIT 1 OFFSET {ind};"
        ret = requests.get(f"http://127.0.0.1:5000/getDataFromTableCommand?command={query}")
        return json.loads(ret.content)

    except Exception as e:
        print("Something wrong with data from requested table ")


def wantedToPush(i):
    wanted = ["management", "Research", "entrepreneurship", "business development", "operations"]
    for j in wanted:
      if Levenshtein.ratio(i,j) > 0.7:
        return True
    return False

def checkWorkers(allWorks):
    ret = []
    for i in range(len(allWorks)):
        tem = allWorks[i].split(" ")
        if len(tem)>1:
            for j in tem:
                if wantedToPush(j) and not i in ret:
                    ret.append(i)
                    continue
        if wantedToPush(allWorks[i]) and not i in ret:
            ret.append(i)
            continue
    return ret

def extractNum(str):
    temp = str.split(" ")
    temp[0] = temp[0].replace(',','')
    return temp[0]

def bundleToDatabase(str,orgUrl):
    try:
        ret = requests.post(f"http://127.0.0.1:5000/pushAllMembersData",data={"data":f"{str}","org":f"{orgUrl}"})
        return ret.content
    except:
        return b"Error"


def run(driver):
    cleanDataIndex = 350
    tem = requests.get("http://127.0.0.1:5000/tableSize?tableName=cleandata")
    tem = json.loads(tem.content)
    tem = tem[0][4]
    while cleanDataIndex < tem :
        try:        
            # fetch data
            currentUrl = getUrl(cleanDataIndex) 
            
            # all windows
            windows = driver.window_handles
            # change driver to window 1
            driver.switch_to.window(windows[0])

            # open new window
            driver.execute_script(f"window.open('{currentUrl[0][2]}')")
            
            # all windows
            windows = driver.window_handles
            # change driver to window 1
            driver.switch_to.window(windows[1])
            
            # wait 10s to load bar 
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script(" return document.getElementsByClassName('org-page-navigation__items ') ") != 'undefined' 
            )
            print("Bar is loaded ...... ")
            time.sleep(2)

            # click to people tag
            script = """
                tem = document.getElementsByClassName("org-page-navigation__items ")[0].children[4].children[0]
                if (!tem.classList.contains("active")){
                    tem.click()
                }
            """
            driver.execute_script(script)
            print("script injected to click on people tag")

            # wait 10s to log to people 
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.getElementsByClassName('artdeco-card org-people-profile-card__card-spacing org-people__card-margin-bottom')[0] ") != 'undefined'
            )
            print("Taged to people ...... ")
            time.sleep(3)

            # click to see more div
            driver.execute_script("document.getElementsByClassName('org-people__show-more-button t-16 t-16--open t-black--light t-bold')[0].click()")
            print("click to see more in people tag .....")
            time.sleep(1)

            # scroll right 
            script = """
                document.getElementsByClassName("artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view artdeco-pagination__button artdeco-pagination__button--next")[0].click()
                document.getElementsByClassName("artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view artdeco-pagination__button artdeco-pagination__button--next")[0].click()
            """
            driver.execute_script(script)

            # search for management, Research, entrepreneurship, business development, operations and click
            time.sleep(1)
            script = """
                tem = document.getElementsByClassName("artdeco-carousel ember-view org-people__carousel-container")[0].children[1].children[0].children[2].children[0].children[0].children[0].children
                temp = Array.from(tem)
                column = []
                temp.forEach((element,index) => {
                    if (index != 0){
                        column.push(element.children[0].children[1].innerText)
                        console.log(element.children[0].children[1].innerText)
                    }
                });
                return JSON.stringify(column)
            """
            allWorks = json.loads(driver.execute_script(script))
            getpositions = checkWorkers(allWorks)
            print("Got the positions ...........")

            getpositions = [x + 1 for x in getpositions]
            print("pos --> ",getpositions)

            # click on the positions
            time.sleep(1)
            script = f"""
                clickPos = {getpositions}
                tem = document.getElementsByClassName("artdeco-carousel ember-view org-people__carousel-container")[0].children[1].children[0].children[2].children[0].children[0].children[0].children
                clickPos.forEach((ele,ind)=>{{
                    tem[ele].click()
                }})
            """
            driver.execute_script(script)
            print("clicked on the positions ....")


            # get the associate member number
            time.sleep(2)
            script = f"""
                return document.getElementsByClassName("org-people__header-spacing-carousel")[0].children[0].innerText
            """
            temp = driver.execute_script(script)
            totalAssoMem = extractNum(temp)
            print("got the total associated members")

            # scroll down till all member are visible
            script = f"""
                function sleep(ms) {{
                    return new Promise(resolve => setTimeout(resolve, ms));
                }}

                allMembers = []
                localStorage.setItem('gotAllMem','None')
                function collectDataLink(){{
                    tem = document.getElementsByClassName("scaffold-finite-scroll__content")[0].children[0].children 
                    temp = Array.from(tem)
                    temp.forEach((ele,ind)=>{{
                        try{{
                            te = ele.children[0].children[0].children[1].children[0].children[0].children[0].href
                            if (te != undefined){{
                                allMembers.push(te)
                            }}
                        }}catch(err){{

                        }}
                    }}) 
                    localStorage.setItem('gotAllMem','done')
                    console.log("allMem -> ",allMembers.length,localStorage.getItem('gotAllMem'))
                }}

                async function scrollRun(){{
                    rollover = true
                    nextLoopCount = 0
                    while (rollover){{
                        tem = document.getElementsByClassName("artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button")
                        if(tem.length > 0){{
                            tem[0].click()
                            console.log("clicked")
                            nextLoopCount = 0
                        }}
                        tem = document.getElementsByClassName("scaffold-finite-scroll__content")[0].children[0].children
                        if ( tem.length >= {totalAssoMem} || nextLoopCount > 10 ){{
                            rollover = false
                            collectDataLink()
                        }}
                        console.log("nextLoop -> ",tem.length,rollover)
                        nextLoopCount = nextLoopCount + 1
                        await sleep(2000)
                    }}
                }}
                scrollRun()
            """
            driver.execute_script(script)
            print("---------------------")
            print("program is going on hold until there is no confirmation of got all member == done")
            print("---------------------")
            WebDriverWait(driver, float('inf')).until(
                lambda d: d.execute_script("return localStorage.getItem('gotAllMem') ") == 'done'
            )   
            print("got all the member in the array in localhost ....")

            # fetch from member array
            time.sleep(1)
            script = """
                return allMembers
            """
            links = driver.execute_script(script)
            print("got the member....")

            # convert links to json string and send it to database api to handle the inputs in mysql
            time.sleep(1)
            if bundleToDatabase(links,currentUrl[0][2]) == b"Error":
                raise Exception("something went wrong while appending in mysql in ",currentUrl[0][2])
            print("send the links to database without errors..........")
            
        except Exception as e:
            print("Got an error .......\n",e)
            file = open("wentWrong.txt","a")
            file.write(f"\n{currentUrl[0][2]}")
            file.close()
        
        # close window
        driver.close()
        # driver point back to window 1
        driver.switch_to.window(windows[0])

        print("cleanDataIndex - ",cleanDataIndex)
        cleanDataIndex  = cleanDataIndex + 1
        # if input("at the end ") == 'd':
        #     break    

    return
    
