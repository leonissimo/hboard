from flask import Flask, render_template, jsonify, Response, json
from sense_hat import SenseHat
from datetime import datetime
from elasticsearch import Elasticsearch
import time


app = Flask(__name__)
sense = SenseHat()
es = Elasticsearch(['http://192.168.0.21:9200'])

@app.route('/')
def index():
    sense = SenseHat()
    t = sense.get_temperature()
    data = get_current_data()
    return render_template('dashboard.html', data=data)

@app.route('/temp')
def temp():
    sense = SenseHat()
    t = sense.get_temperature_from_pressure()
    return jsonify(temperature=str(round(t, 1)))


@app.route('/current')
def current():
    data = get_current_data()
    js = json.dumps(data)

    return Response(js, status=200, mimetype='application/json')

def get_current_data():

    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()
    tp = sense.get_temperature_from_pressure()
    data = {
        'temperature':str(round(t, 1)),
        'pressure':str(round(p,1)),
        'humidity':str(round(h,1)),
        'temperatureP':str(round(tp,1)),
        'datetime' : datetime.now()
    }
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

