from flask import Flask, render_template, request, Response, jsonify, make_response 
from flask_cors import CORS
import datetime
import asyncio
import websockets
import json


import board
import adafruit_bme680

i2c = board.I2C()
BME680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

BME680.sea_level_pressure = 1017

PORT = 8765
DATA_DELAY_SECONDS = 5 # how many seconds would you like to delay before sending?

def C_to_F(temp):
    return ((temp * 1.8) + 32)

app = Flask(__name__, template_folder='templates')

@app.route("/")
 def home():
    now = datetime.datetime.now()
    timeString = now.strftime("%d-%m-%Y %H:%M")
    temp, humidity, pressure, gas=read_sensor()
    templateData = {
       'title' : 'PLANT-BOX READINGS',
       'time': timeString,
       'temp': temp,
       'humidity': humidity,
       'pressure': pressure,
       'gas': gas
       }
    return render_template('index.html', **templateData)


 def read_sensor(*args):
     try:
        temp ='{0:0.2f}'.format(C_to_F(BME680.temperature))
        humidity ='{0:0.2f}'.format(BME680.humidity)
        pressure ='{0:0.2f}'.format(BME680.pressure)
        gas ='{0:0.2f}'.format(BME680.gas)
       
        return temp, humidity, pressure, gas

     except Exception as e:
        print ('error '+str(e))

async def send_ws_msg(websocket):
    while True:
        now = datetime.datetime.now()
        timeString = now.strftime("%m/%d/%Y, %H:%M:%S %p")
        
        temp, humidity, pressure, gas=read_sensor()
        import random
        plantData = dict({ 
            
            'time': timeString,

            temp: temp,
            humidity: humidity
            pressure: pressure,
            gas: gas,

            #'temp': f'{random.random()*100}',
            #'humidity': '97.01',
            #'pressure': '993.89',
            #'gas': '4114.00',
        })
        data_string = json.dumps(plantData)
        await websocket.send(data_string)
        await asyncio.sleep(DATA_DELAY_SECONDS)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    print(f'Starting Websocket server listening on port {PORT}')
    start_server = websockets.serve(send_ws_msg, 'localhost', PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

