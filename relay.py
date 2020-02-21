from flask import Flask, request
from flask_cors import CORS
import json
import time
import RPi.GPIO as GPIO

app = Flask(__name__)
CORS(app)

@app.route("/api/RelayControll", methods=["GET"])
def index():
    with open('config.json') as json_file:
        config = json.load(json_file)
        machine_id = config["machine_id"]
        relay_pin = config['RELAY_PIN']
        relay_switch_time = config["RELAY_SWITCH_TIME"]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay_pin, GPIO.OUT)
        DateNow = time.localtime()
        try:
            GPIO.output(relay_pin,  GPIO.HIGH)   # Turn motor on
            time.sleep(relay_switch_time)
            GPIO.output(relay_pin, GPIO.LOW)  # Turn motor
            msg = "Call Relay success"
        except Exception as e:
            msg = e

        if  (request.headers.getlist("X-Forwarded-For")):
           ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr

        f = open('log.txt','a')
        log = 'machine: {0},message:{1},ip:{2},time:{3}\r\n'.format(machine_id,msg,ip,DateNow)
        f.write(log )

        return  json.dumps({
                "machine": machine_id,
                "msg": msg
        })

if __name__ == '__main__':
    app.debug = False
    app.run(host='127.0.0.1', port=5000 ,debug=False)