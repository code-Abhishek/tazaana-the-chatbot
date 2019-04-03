from flask import Flask, request, make_response, jsonify
import requests
import dialogflow
import json
import sys

import os
import psycopg2
import pandas


try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    print("--------------> I am trying toget DB!")
    print(conn)
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)
finally:
    print("Final")

def insertQuery(dicted, conn):
    try:
        cursor = conn.cursor()
        #dont touch# postgreSQL_select_Query = """INSERT INTO userinfo(username, userage, useremail, userfavcategory, userfavcolor, usernumberofvisits, usergender, userbuysnumber, userfavmaterial, userpricerange, userfavsaleperiod, userid, userfavbrand) VALUES ('Scarlett Johansson', 27, 'aishwarya@rorya.com', 'Heels', 'Black','once a week','F','Never','Cotton','I dont buy', 'Summer Sale', 780, 'Metro');"""
        postgreSQL_noselectttie = "select * from userinfo"
        postgreSQL_insert_Query = str('INSERT INTO userinfo(username, userage, useremail, userfavcategory, userfavcolor, usernumberofvisits, usergender, userbuysnumber, userfavmaterial, userpricerange, userfavsaleperiod, userfavbrand) VALUES ('+ dicted['username'] +','+ dicted['userage'] +','+ dicted['useremail'] +','+ dicted['userfavcategory'] +','+ dicted['userfavcolor'] +','+ dicted['usernumberofvisits'] +','+ dicted['usergender'] +','+ dicted['userbuysnumber'] +','+ dicted['userfavmaterial'] +','+ dicted['userpricerange'] +','+ dicted['userfavsaleperiod'] +','+ dicted['userfavbrand'] +');')
        print("------------------> we are going to show!!")
        cursor.execute(postgreSQL_noselectttie)
        print("------------------> we are going to insert!!")
        cursor.execute(postgreSQL_insert_Query)
        print("insert update")
        print("Selecting rows from userinfo table using cursor.fetchall")
        user_data = cursor.fetchall() 
        print("Print each row and it's columns values")
        for row in user_data:
            print("entry = ", row[0] )
            print("age = ", row[1])
            # print("kuch = ", row[5])
            # print("kuchtohbhi = ", row[6])
            # print("gender  = ", row[2], "\n")
        conn.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into userinfo table")
    except (Exception, psycopg2.Error) as error :
        # print ("Error while fetching data from PostgreSQL", error)
        if(conn):
            print("Failed to insert record into user table", error)
    finally:
        #closing database connection.
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")



# Flask app should start in global layout
app = Flask(__name__)
log = app.logger

#df = pandas.read_csv('Karma.csv') # declaring a matrix of rows and columns

global dicted 
dicted = {}

@app.route('/')
def index():

    return "Hello world!"


'''def setname(gotname):

    global name3
    name3 = str(gotname)
'''

'''def getname():

    return final_name'''



@app.route('/webhook', methods=['GET', 'POST'])
def webhook(): # called by dialogflow for user replies
    
    req = request.get_json(force=True) # the user input to dialogflow
    print(req)
    action = req.get('queryResult').get('action')
    
    res = 0
    
    #name1 = "k"
    #global final_name
    #m = "pandu'sfan"


    if (action == 'age'):
        username = req.get('queryResult').get('queryText')
        dicted['username'] = username
         
        #final_name = rough_name
        #setname(rough_name)
        #name1 = final_name
        res = age(req)

    elif (action == 'email_id'):
        userage = req.get('queryResult').get('queryText')
        userage = userage
        dicted['userage'] = userage

        #ageresponse = req.get('queryResult').get('queryText')
        # sending ageresponse to another python file in the same directory
        #name1 = getname()
        res = emailid(req)

    elif (action == 'gender'):
        useremail = req.get('queryResult').get('queryText')
        dicted['useremail'] = useremail
        #name1 = getname()
        res = gender()


    elif (action == 'categorywrtgender'):
        usergender = req.get('queryResult').get('queryText')
        dicted['usergender'] = usergender
        #name1 = getname()
        if req.get('queryResult').get('queryText') == "Female":
            res = femalecategory()
        elif req.get('queryResult').get('queryText') == "Male":
            res = malecategory()
    
    elif (action == 'femalecategoryselected'):
        userfavcategory = req.get('queryResult').get('queryText')
        dicted["userfavcategory"] = userfavcategory
        if req.get('queryResult').get('queryText') == "Flats":
            #name1 = final_name
            res = flats()
        elif req.get('queryResult').get('queryText') == "Heels":
            #name1 = final_name
            res = heels()
        elif req.get('queryResult').get('queryText') == "Wedges":
            #name1 = final_name
            res = wedges()
    
    

    
    elif (action == 'malecategoryselected'):
        userfavcategory = req.get('queryResult').get('queryText')
        dicted["userfavcategory"] = userfavcategory
        if req.get('queryResult').get('queryText') == "Formal":
            #name1 = final_name
            res = formal()
        elif req.get('queryResult').get('queryText') == "Casual":
            #name1 = final_name
            res = casual()
        elif req.get('queryResult').get('queryText') == "Sports":
            #name1 = final_name
            res = sports()

    elif (action == 'color'):
        userfavbrand = req.get('queryResult').get('queryText')
        dicted["userfavbrand"] = userfavbrand

        #name1 = final_name
        res = color()

    elif (action == 'howmanyvisits'):
        userfavcolor = req.get('queryResult').get('queryText')
        dicted['userfavcolor']=userfavcolor
        res = howmanyvisits()

    elif (action == 'howoftenbuy'):
        usernumberofvisits = req.get('queryResult').get('queryText')
        dicted["usernumberofvisits"] = usernumberofvisits
        res = howoftenbuy()
    
    elif (action == 'material'):
        userbuysnumber = req.get('queryResult').get('queryText')
        dicted['userbuysnumber'] = userbuysnumber
        res = material()

    elif (action == 'pricerange'):
        userfavmaterial = req.get('queryResult').get('queryText')
        dicted['userfavmaterial'] = userfavmaterial
        res = pricerange()

    elif (action == 'campaign'):
        userpricerange = req.get('queryResult').get('queryText')
        dicted['userpricerange'] = userpricerange
        res = campaign()

    elif (action == 'finalintent'):
        userfavsaleperiod = req.get('queryResult').get('queryText')
        dicted['userfavsaleperiod'] = userfavsaleperiod
        res = finalintent()




    elif (action == 'sinkinstallationtypes'):
        res = allsinkinstallationtypes(req), 
    return make_response(jsonify(res))

    
def age(req):
    #NAME = req.get('queryResult').get('queryText')
    mytextRes = "Please enter your age as suggested :"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "15"},{"title": "26"},{"title": "38"}]}}}} 
    print(res)
    return(res)

def emailid(req):
    #ageresponse = req.get('queryResult').get('queryText')
    #df['Age'][0] = ageresponse
    mytextRes =   "Please enter your email id in the format suggested :"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "xyz@gmail.com"},{"title": "xyz@gmail.co.in"}]}}}} 
    return(res)

def gender(): #(req)
    #Category = req.get('queryResult').get('parameters').get('Category')
    mytextRes =  "Please select your gender :"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Male"},{"title": "Female"}]}}}} 
    return(res)

def femalecategory():
    mytextRes = "Please select your favourite category"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Flats"},{"title": "Heels"},{"title": "Wedges"}]}}}} 
    return(res)

def malecategory():
    mytextRes = "Please select your favourite category"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Sports"},{"title": "Casual"},{"title": "Formal"}]}}}} 
    return(res)

def flats():
    mytextRes = "Under Flats category, what is your favourite brand?"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Cara Mia"},{"title": "Beonza"}]}}}} 
    return(res)

def heels():
    mytextRes = "Under Heels category, what is your favourite brand?"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Lavie"},{"title": "Metro"}]}}}} 
    return(res)

def wedges():
    mytextRes = "Under Wedges category, what is your favourite brand?"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Catwalk"},{"title": "Allen Soly"}]}}}} 
    return(res)

def formal():
    mytextRes = "Under Formal category, what is your favourite brand?"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Nike"},{"title": "Puma"}]}}}} 
    return(res)

def casual():
    mytextRes = "Under Casual category, what is your favourite brand?"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Bata"},{"title": "Paragon"}]}}}} 
    return(res)

def sports():
    mytextRes = "Under Sports category, what is your favourite brand?"
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Lee Cooper"},{"title": "Smoky"}]}}}} 
    return(res)

def color():
    mytextRes = "So, what is your favourite colour ? "
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Black"},{"title": "Brown"},{"title": "Blue"}]}}}} 
    return(res)

def howmanyvisits():
    mytextRes = "So, how many times do you visit our website in a week ? "
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Once a week"},{"title": "Twice a week"},{"title": "Thrice a week"},{"title": "More than thrice a week"}]}}}} 
    return(res)

def howoftenbuy():
    mytextRes = "So, how often do you buy our product? "
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Never"},{"title": "Once a week"},{"title": "More than once a week"},{"title": "Once a month"},{"title": "Quarterly"}]}}}} 
    return(res)

def material():
    mytextRes = "So, what is your favourite material? "
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Cotton"},{"title": "Leather"}]}}}} 
    return(res)

def pricerange():
    mytextRes = "So, the products you generally buy lie in which range? "
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "I don't buy"},{"title": "$10 to $20"},{"title": "$21 to $40"},{"title": "$41 to $70"},{"title": "$71 and more"}]}}}} 
    return(res)

def campaign():
    mytextRes = "Finally, during which of our sales did you buy the maximum products? "
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes}}],"suggestions": [{"title": "Christmas Sale"},{"title": "Republic Day"},{"title": "Big Bumper Sale"},{"title": "Independence Day Sale"},{"title": "King Discount Sale"}]}}}} 
    return(res)

'''def femalecategoryselectedfallback():
    res = femalecategory()
    return res
'''

def finalintent():
    mytextRes = "Thank you very much for taking the survey. We hope to see you soon:D"
    insertQuery(dicted,conn) #here we are inserting the data to the store.
    res = {"fulfillmentText": mytextRes,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech": mytextRes , "displayText" : mytextRes}}]}}}} 
    return res


def allsinkinstallationtypes(req):
    brandName = req.get('queryResult').get('parameters').get('Brand')
    mytextRes = "We have following installationtypes for "+ brandName
    res = {"fulfillmentText": mytextRes ,"payload": {"google": {"expectUserResponse": True,"richResponse": {"items": [{"simpleResponse": {"textToSpeech":  mytextRes}}],"suggestions": [{"title": "Drop In"},{"title": "Undermount"},{"title": "Farmhouse"}]}}}} 
    return(res)
    
def getRequest(URL, PARAMS):
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    print(data)

def postRequest(API_ENDPOINT, DATA):
    
    r = requests.post(url = API_ENDPOINT, data = DATA)
    data = r.json()
    print(data)

def apiCall(URL, POSTMAN_TOKEN):
    
    payload = ""
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "login.microsoftonline.com",
        'cache-control': "no-cache",
        'Postman-Token': POSTMAN_TOKEN
        }
    response = requests.request("POST", URL, data=payload, headers=headers)
    print(response.text)

#df.to_csv('Karma.csv')

if __name__ == '__main__':
    app.run()

