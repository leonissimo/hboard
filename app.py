from flask import Flask, render_template, jsonify, Response, json

from datetime import datetime
from elasticsearch import Elasticsearch

try:
    from sense_hat import SenseHat
except ImportError:
    enable_sense_hat = False
import time


app = Flask(__name__)
es = Elasticsearch(['http://192.168.0.21:9200'])

@app.route('/')
def index():
    data = get_current_data()
    return render_template('dashboard.html', data=data)

@app.route('/current')
def current():
    data = get_current_data()
    js = json.dumps(data)

    return Response(js, status=200, mimetype='application/json')



def get_current_data():
    if(enable_sense_hat):
        sense = SenseHat()
        sense.clear()
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
    else:
         data = {
            'temperature': 0,
            'pressure':0,
            'humidity':0,
            'temperatureP':0,
            'datetime' : datetime.now()
         }
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

