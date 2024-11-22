import requests
import json
import os 
import time
import pygetwindow
import pyautogui
from pywinauto import Application
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait


def reqRow(num):
    try:
        personLink = requests.get(f"http://127.0.0.1:5000/getRawRow?table=profpersons&stRow={num}&nums=1")
        return json.loads(personLink.content)[0][1]
    except:
        return "Error"

with open(f"{os.getcwd()}/messaging/message.txt","r") as file:
    content = file.read()

def run(driver):
    with open(f"{os.getcwd()}/messaging/tempData.txt","r") as file:
        pageData = file.read()
    currentPersonNum = int(pageData)
    # 650 hogay tha
    tem = requests.get("http://127.0.0.1:5000/tableSize?tableName=profpersons")
    tem = json.loads(tem.content)
    tem = tem[0][4]
    while currentPersonNum < tem:
        try:
            # all windows
            windows = driver.window_handles
            # change driver to window 1
            driver.switch_to.window(windows[0])
            print("pointing at window 0 .......")

            # request the person profile link
            link = reqRow(currentPersonNum)
            if link == "Error":
                raise Exception("Error in link from mysql")
            print(link)
            print("currPerNum = ",currentPersonNum," | link = ",tem)

            # open new window
            driver.execute_script(f"window.open('{link}')")
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


            futureCom = input("f(for break loop)\nd*(for loading particular page using number)\ns(for skip)\np(for previous)\nany other input to continue \nWaiting for input command >>> ")


            # if you want to skip
            if futureCom == 'f':
                # close window
                driver.close()
                # driver point back to window 0
                driver.switch_to.window(windows[0])
                break
            elif futureCom.isdigit():
                currentPersonNum = int(futureCom)-1
            elif futureCom == 'p':
                currentPersonNum = currentPersonNum -2
            elif futureCom != 's':

                # click on more
                time.sleep(1)
                script = """
                    function sleep(ms) {
                        return new Promise(resolve => setTimeout(resolve, ms));
                    }
                    teLen = document.getElementsByClassName("ph5 pb5")[0]
                    if(teLen == undefined){
                        teLen = document.getElementsByClassName("ph5 ")[0].children.length
                        tem = document.getElementsByClassName("ph5 ")[0].children[teLen-1]
                        if (tem.className == 'display-flex'){
                            tem = document.getElementsByClassName("ph5 ")[0].children[teLen-2]
                        }
                    }else{
                        teLen = document.getElementsByClassName("ph5 pb5")[0].children.length
                        tem = document.getElementsByClassName("ph5 pb5")[0].children[teLen-1]
                        if (tem.className == 'display-flex'){
                            tem = document.getElementsByClassName("ph5 pb5")[0].children[teLen-2]
                        }
                    }
                    len = tem.children[0].children.length
                    temp = tem.children[0].children[len-1]
                    localStorage.setItem("connection","None")
                    async function check(){
                        if(temp.children[1].getAttribute("aria-hidden") == 'true'){
                            temp.children[0].click()
                        }
                        // find and click
                        // search row
                        // fist find remove connection
                        await sleep(2000)
                        remConn = Array.from(temp.children[1].children[0].children[0].children)
                        for(let i=0; i<remConn.length; i++){
                            try{
                                console.log(remConn[i].children[0].children[1].innerText)
                                if(remConn[i].children[0].children[1].innerText == "Remove Connection"){
                                    localStorage.setItem("connection","already")
                                }
                                if(remConn[i].children[0].children[1].innerText == "Pending"){
                                    localStorage.setItem("connection","pending")
                                }
                                if(remConn[i].children[0].children[1].innerText == "Connect"){
                                    remConn[i].children[0].click()
                                    localStorage.setItem("connection","clicked")
                                }
                            }catch(err){
                            }
                        }

                        if(localStorage.getItem("connection")!="already"){
                            row = tem.children[0]
                            ro = Array.from(row.children)
                            for(let i=0; i<ro.length; i++){
                                try{
                                    if(ro[i].children[1]==undefined){
                                        console.log(ro[i].children[0].innerText)
                                        if(ro[i].children[0].innerText == "Connect"){
                                            ro[i].children[0].click()
                                            localStorage.setItem("connection","clicked")
                                        }
                                        if(ro[i].children[0].innerText == "Pending"){
                                            localStorage.setItem("connection","pending")
                                        }
                                        if(ro[i].children[0].innerText == "Remove Connection"){
                                            localStorage.setItem("connection","already")
                                        }
                                    }else{
                                        console.log(ro[i].children[1].innerText)
                                        if(ro[i].children[1].innerText == "Connect"){
                                            ro[i].children[1].click()
                                            localStorage.setItem("connection","clicked")
                                        }
                                        if(ro[i].children[1].innerText == "Pending"){
                                            localStorage.setItem("connection","pending")
                                        }
                                        if(ro[i].children[1].innerText == "Remove Connection"){
                                            localStorage.setItem("connection","already")
                                        }
                                    }
                                }catch(err){
                                }
                            }
                        }
                    }
                    check()
                """
                driver.execute_script(script)
                print("running check() script .....")


                print("checking localStorage for 5s ....")
                time.sleep(5)
                script = """
                    return localStorage.getItem('connection')
                """
                conn = driver.execute_script(script)
                print("conn - ",conn)

                if conn == 'None': 
                    raise Exception("Connection is None")
                elif conn == "already":
                    print("Connection already stablished")
                    pass    
                elif conn == "pending":
                    print("Connection in pending stage")
                    pass
                elif conn == 'clicked':
                    # click add to note
                    script="""
                        document.getElementsByClassName("artdeco-modal__actionbar ember-view text-align-right")[0].children[0].click()
                    """
                    driver.execute_script(script)
                    print("click 'add to note' button ....... ")


                    win = pygetwindow.getWindowsWithTitle('Chrome')
                    pos = None
                    for w in range(len(win)): 
                        if win[w].title[:6] == driver.title[:6]:
                            pos = w
                            break
                        
                    # click on particular chrome window
                    app = Application().connect(title=win[pos].title)
                    app[win[pos].title].set_focus()
                    print("set the chrome window on focus ......")

                    # click on textarea
                    time.sleep(2)
                    ele = driver.find_element(By.ID,"custom-message")
                    locat = ele.location
                    app[win[pos].title].set_focus()
                    pyautogui.moveTo(int(win[pos].topleft[0])+int(locat['x'])+100 , int(win[pos].topleft[1])+int(locat['y'])+300)
                    pyautogui.click()
                    print("click on textarea .......")

                    # copy note and send
                    time.sleep(1)
                    global content
                    script = f"""
                        tem = document.getElementById("custom-message")
                        tem.value = '{content}'
                    """
                    driver.execute_script(script)
                    print("content copied ....... ")


                    # escape click()
                    time.sleep(1)
                    app[win[pos].title].set_focus()
                    pyautogui.moveTo(int(win[pos].topleft[0])+int(locat['x'])+100 , int(win[pos].topleft[1])+int(locat['y'])+1200)
                    pyautogui.click()
                    print("click on escape textarea .........")

                    # clicking send
                    time.sleep(1)
                    script = f"""
                        tem = document.getElementById("custom-message")
                        tem.parentElement.parentElement.parentElement.parentElement.children[4].children[2].click()
                    """
                    driver.execute_script(script)
                    print("click on send button and waiting for 5s......")
                    time.sleep(5)



                else:
                    raise Exception("nothing came up in conn")



        except Exception as e:
            print("In the exception => ",e)
            file = open(f"{os.getcwd()}/messaging/somethingWentWrong.txt","a")
            file.write(f"\n{link}")
            file.close()


        # input or sleep and toggle break
        # input("At the end ")
        # time.sleep(10)

        # close window
        driver.close()
        # driver point back to window 0
        driver.switch_to.window(windows[0])

        currentPersonNum  = currentPersonNum + 1
        with open(f"{os.getcwd()}/messaging/tempData.txt","w") as file:
            file.write(f"{currentPersonNum}")
        
        # toggle break
        # break


    return 