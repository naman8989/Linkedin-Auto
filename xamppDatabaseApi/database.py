from flask import Flask , request
from flask_cors import CORS
import mysql.connector
import json

app = Flask(__name__)
CORS(app)

try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="linkedin"  
    )
except:
    print("mysql server is close")


def sqlCommitWorkFlow(quer):
    try:
        mycursor = mydb.cursor()

        mycursor.execute(quer)
        mydb.commit()
        row = mycursor.fetchall()

        mycursor.close()
        return row
    
    except mysql.connector.Error as err:
        print("err from mysql",err)
        return "Error"

def sqlWorkFlow(quer):
    try:
        mycursor = mydb.cursor()

        mycursor.execute(quer)
        row = mycursor.fetchall()

        mycursor.close()
        return row
    
    except mysql.connector.Error as err:
        print("err from mysql",err)
        return "Error"



app = Flask(__name__) #creating the Flask class object   
 
@app.route('/')
def home():
    return "api is working"

@app.route('/companyData') #decorator drfines the   
def companyData():

    try:
        companyName = request.args.get('cn')
        companyLocation = request.args.get('cl')
        companyUrl = request.args.get('cu')
        # print(companyName,companyLocation,companyUrl)
        mycursor = mydb.cursor()
        query = f"INSERT INTO allcompanydata(Name,Location,URL) VALUES ('{companyName}','{companyLocation}','{companyUrl}')"
        mycursor.execute(query)
        mydb.commit()
        row = mycursor.fetchall()

        mycursor.close()
        
        print("----------")
        return row

    except mysql.connector.Error as err:
        print("err from mysql",err)
        return "Error"
    
@app.route('/getRawRow')
def getRawRow():
    whichTable = request.args.get('table')
    startRow = request.args.get('stRow')
    nums = request.args.get('nums')
    query = f"SELECT * FROM {whichTable} LIMIT {nums} OFFSET {startRow}"
    return sqlWorkFlow(query)

@app.route('/tableSize')
def getTableSize():
    tableName= request.args.get('tableName')
    query = f"SHOW TABLE STATUS LIKE '{tableName}';"
    print("-----------")
    print(sqlWorkFlow(query))
    return sqlWorkFlow(query)

@app.route("/pushDatatoTable")
def pushTableData():
    totalInp = int(request.args.get('totalInp'))
    table = request.args.get('useTable')
    locations = request.args.get('location')
    locData = request.args.get('data')
    locData = locData.split('|')
    loc = "("+ locations +")"
    values = ""
    while totalInp != 0:
        subData = locData[totalInp-1].split(',')
        temp = "" 
        for i in subData:
            temp = temp + "'" + i + "'" + ","
        temp = temp[:len(temp)-1]
        values = values + "(" + f"{temp}" + "), "
        totalInp = totalInp - 1
    values = values[:len(values)-2] 
    query = f"INSERT INTO {table} {loc} VALUES {values} "
    print("quer - ",query)
    print("-------------")
    return sqlCommitWorkFlow(query)

@app.route("/getDataFromTableCommand")
def getTableData():
    query = request.args.get("command")
    print(query)
    return sqlWorkFlow(query)
    
@app.route("/pushAllMembersData", methods=['POST'])
def disectAndPushData():
    try:
        data = request.form.get("data")
        org = request.form.get("org")
        str1 = data.strip()[1:-1]
        st = str1.split(",")
        
        vals = ""
        for i in st:
            vals += f"('{org}',{i}),"
        vals = vals[:-1]
        quer = f"""
            INSERT INTO peoplelinks (orginal, links)
            VALUES
                {vals}
        """
        quer = quer[:-1]
        print("qu -> ",quer)

        mycursor = mydb.cursor()
        mycursor.execute(quer)
        mydb.commit()
        row = mycursor.fetchall()
        mycursor.close()
        
        return "got it "

    except Exception as e:
        return "Error"

    
  
if __name__ =='__main__':  
    if mydb.is_connected():
        app.run(debug = True)  
        mydb.close()


