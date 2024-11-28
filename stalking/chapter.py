import json
import time
from selenium.webdriver.support.ui import WebDriverWait



def run(driver):

    # all windows
    windows = driver.window_handles
    # change driver to window 1
    driver.switch_to.window(windows[0])
    print("pointing at window 0 .......")

    currUrl = "https://www.linkedin.com/in/solennesavoia/"

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

            name = teLen[0].children[0].children[0].innerText
            allRoles = teLen[0].children[1].innerText
            currentLocation = teLen[2].children[0].innerText

            aboutPerson = document.getElementsByClassName("display-flex ph5 pv3")[0].children[0].children[0].children[0].children[1].innerText

            exp = document.getElementById("experience").parentElement.children[2].children[0]
            exp = Array.from(exp.children)
            expData = []
            exp.forEach((ele,ind)=>{
                expData.push(ele.children[0].children[1].innerText)
            })

            previousCompany = []
            exp.forEach((ele,ind)=>{
                previousCompany.push(ele.children[0].children[0].children[0].href)
            })
            
            await sleep(2000)
            localStorage.setItem('personData',JSON.stringify([window.location.href,name,allRoles,currentLocation,aboutPerson,expData,previousCompany]))
        }
        retData()
    """
    driver.execute_script(script)
    print("running to get person data........")

    
    time.sleep(3)
    script = """
        return localStorage.getItem('personData')
    """
    personData = driver.execute_script(script)
    print("waiting for 3 second to localstorage return data........")


    # close the tab and rearrage

    # algo to get format personData




    # scrap activity page
    currUrl += "recent-activity/all/"
    
    # open tab script


    # get post data script
    script = """
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        postData = []
        async function retrive(){
            acts = document.getElementsByClassName("pv0 ph5")[1].children[0].children[0].children[0].children[1].children
            acts = Array.from(acts)
            acts.forEach((ele,ind)=>{
                postData.push(ele.children[0].children[0].innerText)
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
    print("waiting for 3 second to localstorage return data........")

    # close the tab



    # open the current company site
    script = """
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        async function companyData(){
            bar = document.getElementsByClassName("org-page-navigation__items ")[0].children
            bar = Array.from(bar)
            for(let i=0; i<bar.length; i++){
                head = bar[i].chidlren[0].innerText
                if(head == 'Alumni' || head == 'People'){
                    bar[i].children[0].click()
                    break;
                }
            }
            await sleep(4000)
            totalPeople = document.getElementsByClassName("org-people__insights-container org-people__insights-container--is-collapsed")[0].children[0].children[0].children[0].children[0].children[0].children[0].innerText
            localStorage.setItem('companyNum',JSON.stringify(totalPeople))
        }
        companyData()
    """
    driver.execute_script(script)
    print("executing company function ........")


    script="""
        return localStorage.getItem('companyNum')
    """
    companyStrength = driver.execute_script(script)
    print("fetching company strength ........ ")
    



    # close window
    driver.close()
    # driver point back to window 0
    driver.switch_to.window(windows[0])

    return


