import json
import time
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait

def reqRow(num):
    try:
        personLink = requests.get(f"http://127.0.0.1:5000/getRawRow?table=profpersons&stRow={num}&nums=1")
        return json.loads(personLink.content)[0][1]
    except:
        return "Error"

def repeatCheck(st):
    
    retSt = ""
    prevSt = ""
    with open("repeatCheck.txt","w") as file:
        file.write(st)
    try:
        with open("repeatCheck.txt","r",encoding="utf-8",errors="replace") as file:
            for curLine in file:
                if curLine != prevSt:
                    retSt += curLine
                prevSt = curLine
    except:
        return
    return retSt
    
def breakCheck(st):
    allLine = st.split("\n")
    ret = ""
    prev = ""
    for i in allLine:
        try:
            if prev != i:
                ret += i + "\n"
            prev = i
        except:
            continue
    return ret

def run(driver):
    
    with open(f"{os.getcwd()}/stalking/tempData.txt","r") as file:
        pageData = file.read()
    startUrlNum = int(pageData)
    endUrlNum = requests.get("http://127.0.0.1:5000/tableSize?tableName=profpersons")
    endUrlNum = json.loads(endUrlNum.content)
    endUrlNum = endUrlNum[0][4]

    while(startUrlNum<=endUrlNum):
        currUrl = reqRow(startUrlNum)
        if currUrl == "Error":
            return

        try:

            print("Current Url: ",currUrl)
            # all windows
            windows = driver.window_handles
            # change driver to window 1
            driver.switch_to.window(windows[0])
            print("pointing at window 0 .......")


            # open new window
            driver.execute_script(f"window.open('{currUrl}')")
            print("open person link .......")

            # all windows
            windows = driver.window_handles
            # change driver to window 1
            driver.switch_to.window(windows[1])
            print("pointing at window 1 ......")

            # check for page loaded or not
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            ) 
            print("page loaded.....")

            # scraping person info
            time.sleep(1)
            script = """
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }
                async function retData(){

                    teLen = document.getElementsByClassName("ph5 pb5")[0]
                    if(teLen == undefined){
                        teLen = document.getElementsByClassName("ph5 ")[0].children[1].children

                    }else{
                        teLen = document.getElementsByClassName("ph5 pb5")[0].children[1].children
                    }

                    try{
                        name = teLen[0].children[0].children[0].innerText
                    }catch(err){
                        name = ""
                    }
                    try{
                        allRoles = teLen[0].children[1].innerText
                    }catch(err){
                        allRoles = ""
                    }
                    try{
                        currentLocation = teLen[2].children[0].innerText
                    }catch(err){
                        currentLocation = ""
                    }
                    try{
                        aboutPerson = document.getElementsByClassName("display-flex ph5 pv3")[0].children[0].children[0].children[0].children[1].innerText
                    }catch(err){
                        aboutPerson = ""
                    }

                    exp = document.getElementById("experience").parentElement.children[2].children[0]
                    exp = Array.from(exp.children)
                    expData = []
                    exp.forEach((ele,ind)=>{
                        try{
                            expData.push(ele.children[0].children[1].innerText)
                        }catch(err){
                            expData.push("")
                        }
                    })

                    previousCompany = []
                    exp.forEach((ele,ind)=>{
                        try{
                            previousCompany.push(ele.children[0].children[0].children[0].href)
                        }catch(err){
                            previousCompany.push("")
                        }
                    })

                    await sleep(2000)
                    localStorage.setItem('personData',JSON.stringify([window.location.href,name,allRoles,currentLocation,aboutPerson,expData,previousCompany]))
                }
                retData()
            """
            driver.execute_script(script)
            print("running to get person data........")


            # ret scraped data from localstorage
            time.sleep(3)
            script = """
                return localStorage.getItem('personData')
            """
            personData = driver.execute_script(script)
            print("waiting for 3 second to localstorage return data........")
            personData = json.loads(personData)
            
            # reset current url
            currUrl = personData[0]
            
            # close the tab and rearrage
            # close window
            driver.close()
            # driver point back to window 0
            driver.switch_to.window(windows[0])
            print("rearranging tabs ..........")


            # algo to get format personData
            personData[4] = breakCheck(personData[4])
            for pd in personData[5]:
                pd = breakCheck(pd)
                


            # scrap activity page
            actUrl = currUrl+"recent-activity/all/"
            print(actUrl)

            # open tab script
            # open new window
            driver.execute_script(f"window.open('{actUrl}')")
            print("open person link .......")

            # all windows
            windows = driver.window_handles
            # change driver to window 1
            driver.switch_to.window(windows[1])
            print("pointing at window 1 ......")

            # check for page loaded or not
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            ) 
            print("page loaded.....")

            # column check
            time.sleep(1)
            WebDriverWait(driver,10).until(
                lambda d: d.execute_script("return document.getElementsByClassName('pv0 ph5')[1].innerText") != ""
            )

            # get post data script
            time.sleep(2)
            script = """
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }
                postData = []
                async function retrive(){
                    acts = document.getElementsByClassName("pv0 ph5")[1].children[0].children[0].children[0].children[1].children
                    acts = Array.from(acts)
                    acts.forEach((ele,ind)=>{
                        try{
                            postData.push(ele.children[0].children[0].innerText)
                        }catch(err){
                            postData.push("")
                        }
                    })
                    await sleep(2000);
                    localStorage.setItem('allPost',JSON.stringify(postData))
                }
                retrive()
            """
            driver.execute_script(script)
            print("running to get person post data ...........")


            time.sleep(3)
            script = """
                return localStorage.getItem('allPost')
            """
            personPostData = driver.execute_script(script)
            personPostData = json.loads(personPostData)
            print("waiting for 3 second to localstorage return data........")
            # print(personPostData)
            for ppd in personPostData:
                ppd = breakCheck(ppd)
            

            
            # close the tab
            # close window
            driver.close()
            # driver point back to window 0
            driver.switch_to.window(windows[0])


            # open the current company site
            comUrl = personData[6][0]
            print("company Url: ",comUrl)
            # open new window
            driver.execute_script(f"window.open('{comUrl}')")
            print("open person link .......")

            # all windows
            windows = driver.window_handles
            # change driver to window 1
            driver.switch_to.window(windows[1])
            print("pointing at window 1 ......")

            # check for page loaded or not
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            ) 
            print("page loaded.....")


            # scrap the data from current company site
            time.sleep(1)
            script = """
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }
                async function companyData(){
                    bar = document.getElementsByClassName("org-page-navigation__items ")[0].children
                    bar = Array.from(bar)
                    for(let i=0; i<bar.length; i++){
                        try{
                            head = bar[i].children[0].innerText
                            if(head == 'Alumni' || head == 'People'){
                                bar[i].children[0].click()
                                break;
                            }
                        }catch(err){
                        }
                    }
                    await sleep(4000)
                    try{
                        totalPeople = document.getElementsByClassName("org-people__insights-container org-people__insights-container--is-collapsed")[0].children[0].children[0].children[0].children[0].children[0].children[0].innerText
                    }catch(err){
                        totalPeople = ""
                    }
                    localStorage.setItem('companyNum',JSON.stringify(totalPeople))
                }
                companyData()
            """
            driver.execute_script(script)
            print("executing company function ........")

            # get company info
            time.sleep(5)
            script="""
                return localStorage.getItem('companyNum')
            """
            companyStrength = driver.execute_script(script)
            print("fetching company strength ........ ")
            print(companyStrength)

            

            tem = requests.get(f"http://127.0.0.1:5000/pushPersonData?personUrl={personData[0]}&personName={personData[1]}|{companyStrength}&personAllRoles={personData[2]}&personCurrLoc={personData[3]}&personAbout={personData[4]}&personExp={personData[5]}&personPrevCom={personData[6]}&personPostData={personPostData}")
            if tem == "Error":
                raise Exception("data is not stored")

            
        except Exception as e:
            print("In the exception => ",e)
            file = open(f"{os.getcwd()}/stalking/somethingWentWrong.txt","a")
            file.write(f"\n{currUrl}")
            file.close()

        # close window
        driver.close()
        # driver point back to window 0
        driver.switch_to.window(windows[0])
        print("\n\n")
        
        startUrlNum += 1
        with open(f"{os.getcwd()}/stalking/tempData.txt","w") as file:
            file.write(f"{startUrlNum}")

        time.sleep(3)
        print("in sleep for terminate")


    return


