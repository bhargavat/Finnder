# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
import os
from twilio.rest import Client
#from pymongo import MongoClient
import pymongo
#from pymongo import collection
from bson.objectid import ObjectId
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import time

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://root:3yugrClaWa65KNu6Bx89@ds231658.mlab.com:31658/heroku_5m03dtnw')
db = client.heroku_5m03dtnw

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply(): #sell
    user_input = request.form['Body']
    array = user_input.split(' ')
    if array[0].lower() == 'sell':
        resp = MessagingResponse()
        city = request.values['FromCity']
        state = request.values['FromState']
        country = request.values['FromCountry']
        zip = request.values['FromZip']
        phonenumber = request.values['From']
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        resp.message("This is a reply")
        post = {"location": {"city": format(city),"state": format(state), "country": format(country), "zip": format(zip)},
                "amount": "$"+array[2], "phoneNumber": phonenumber,"fishName": array[1], "dateEntered": str(timestamp)}
        sell = db.sells
        sale = sell.insert_one(post).inserted_id

        return str(resp)
    elif array[0].lower() == 'setup':
        resp = MessagingResponse()
        city = request.values['FromCity']
        resp.message("Thank you for messaging from " + format(city))
        post = {"city:" : format(city)}
        sell = db.SellList
        sale = sell.insert_one(post).inserted_id
        return str(resp)
    elif array[0].lower() == 'selllist':
        resp = MessagingResponse()
        sell = db.sells
        country = request.values['FromCountry']
        print(country)
        fishName = array[1]
        sale = sell.find({"fishName": fishName, "location.country": country}).sort('dateEntered', pymongo.DESCENDING)
        print(sale.count())
        sale_str = ""
        for obj in sale[0:5]:
            id = str(obj["_id"])
            sale_str += "\n"+str(obj['fishName']) + " selling for " + str(obj['amount']) + " id: " + id[len(id)-4:]
        resp.message(sale_str)
        #sale = sell.insert_one(post).inserted_id
        return str(resp)
    elif array[0].lower() == 'info':
            resp = MessagingResponse()
            sell = db.sells
            idNumber = "5a7fb66cbf10c7c8c3f0"+str(array[1])
            sale = sell.find({"_id" : ObjectId(idNumber)})
            resp.message("Please contact: " + sale[0]['phoneNumber'])
            return str(resp)

def sumFish():
    sell = db.sells
    sales = sell.find()
    sum = 0
    for object in sales:
        sum = sum + float(object['amount'][1:])
    print("The sum is " + str(sum))
    return sum


if __name__ == "__main__":
    app.run(debug=True)

# Find these values at https://twilio.com/user/account
# account_sid = "ACed9dae8c07d3775051f48b736a74f301"
# auth_token = "da8ab51db8a8de1129f5b332dd4e8307"


# client = Client(account_sid, auth_token)
#
# client.api.account.messages.create(
#     to="+14084803304",
#     from_="+18312221861",
#     body="Hi! Please enter your city")

