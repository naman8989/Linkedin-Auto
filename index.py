import os 
import importlib

def run(driver):
    curFolder = ""
    while curFolder != 'f':
        folders = [f for f in os.listdir('.') if os.path.isdir(f)] 
        for i in range(len(folders)):
            print(i," | ",folders[i])

        curFolder = input("Please login into your account if not\nEnter the folder initial 4 letter or index number to call | Press (f) to exit >> ")
        if curFolder == 'f':
            continue

        try:
            curFolder = folders[int(curFolder)]
        except:
            for i in folders:
                if i[:4] == curFolder[:4]:
                    curFolder = i
                    break
    
        print(f"loading {curFolder} / chapter")
        fileFunc = importlib.import_module(f"{curFolder}.chapter")
        fileFunc = importlib.reload(fileFunc)

        print(f"poking the run() function in {curFolder} / chapter")
        fileFunc.run(driver)

    
    print("in the index.py end")
    