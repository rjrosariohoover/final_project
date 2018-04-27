import random
import requests
import json
from flask import (Flask,
                   request,
                   url_for,
                   render_template,)
import serial

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/data.json")
def data():
    # TODO read temperature and humidity from Arduino
    ser = serial.Serial("/dev/ttyACM7", timeout=1)
    l = ser.readline()
    x = l.strip().split(",")
    indoor_temp = x[0]
    indoor_humidity = x[1]
    # TODO read temperature and humidity from openweathermap.org
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?id=4347242&units=imperial&appid=07bb18e0fe08bca1ad213f9ac70f5f06")
    data = r.json()
    outdoor_temp = data['main']['temp']
    outdoor_humidity = data['main']['humidity']
    # send the result as JSON
    return json.dumps({
        "indoor_temp": indoor_temp,
        "indoor_humidity": indoor_humidity,
        "outdoor_temp": outdoor_temp,
        "outdoor_humidity": outdoor_humidity})


@app.route("/cheep",methods=['POST'])
def cheep():
    name = request.form['name']
    message = request.form['message']
    print("got a cheep from [%s]: %s" % (name,message))
    # TODO: arduino.write(message) LOL ARDUINO DOESN'T WORK
    with open("cheeps.log",'a') as f:
      f.write("%s: %s" %(name,message))
      f.write("\n")
    # TODO: display the cheep on the kit LCD
    return render_template('thankyou.html')
