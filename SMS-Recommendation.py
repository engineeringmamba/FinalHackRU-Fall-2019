# HackRU Fall 2019
# SMS Recommendation
# Uses Google Places API to get nearby locations through sms instead of data
# Authors:
# Sohan Ganguli (@engineeringmamba)
# Krzysztof Grochal (@KrzysGro)
# ZiJun Weng (@AtelierSilver)
#
import googlemaps
import requests
import json
import pycodestyle
import ssl
from uszipcode import SearchEngine
from twilio.rest import Client
from flask import Flask, request, redirect, session
from twilio.twiml.messaging_response import MessagingResponse
client = Client('Client_API', 'API_Secret')  # nopep8

message = client.messages.create(to='+16097053245', from_='+17325851951', body='please enter what you are looking for and the zipcode. Keyword, Zip_Code')  # nopep8
print(message.sid)

app = Flask(__name__)

resp = MessagingResponse()


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    number = request.form['From']
    body = request.form['Body']
    print(body)
    print('uhh this works?')
    word = body.split(',')
    keyword = word[0]
    zip_code = word[1]

    getPlaces(zip_code, keyword)
    return str(resp)


def getPlaces(zipcode, keywrd):

    print(zipcode)
    print(keywrd)

    api_key = 'GOOGLE-API-KEY'
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    search = SearchEngine(simple_zipcode=True)
    zipcode = search.by_zipcode(zipcode)

    zipcode.to_dict()

    longlat = (str(zipcode.lat) + "," + str(zipcode.lng))
    print(longlat)

    response = requests.get(
        url + 'query=' + keywrd + '&key=' + api_key + '&locationbias=circle&radius=3000&location=' + longlat)  # nopep8

    json_obj = response.json()

    results = json.dumps(json_obj['results'])
    results = json.loads(results)
    data = ['place_id', 'formatted_address', 'name', 'opening_hours']
    places = []

    print(data)

    for x in range(0, 5):
        item = {key: value for (key, value)
                in results[x].items() if key in data}
        places.append(item)

    for i in range(0, 5):
        resp.message(str((formatPlace(places[i]))))

    return data


def formatPlace(dict):
    for item in dict:
        if "opening_hours" in dict:
            return dict['name'] + "\n" + dict['formatted_address'] + "\nOpen Now: " + "Yes" if dict['opening_hours']['open_now'] else "No"  # nopep8


if __name__ == "__main__":
    app.run(debug=False)
