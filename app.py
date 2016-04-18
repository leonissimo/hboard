from flask import Flask, render_template, jsonify, Response, json
from flask_socketio import SocketIO, send, emit


from datetime import datetime
from elasticsearch import Elasticsearch
from threading import Thread, Event
import time


try:
    from sense_hat import SenseHat
    enable_sense_hat = True
except ImportError:
    enable_sense_hat = False



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
es = Elasticsearch(['http://192.168.0.21:9200'])

thread = Thread()
thread_stop_event = Event()

class LiveThread(Thread):
    def __init__(self):
        self.delay = 1
        super(LiveThread, self).__init__()

    def live(self):
        data = get_current_data()
        print "Making random numbers"
        while not thread_stop_event.isSet():
            print 'new'
            js = json.dumps(data)
            socketio.emit('live', js)
            time.sleep(10)

    def run(self):
        self.live()

@app.route('/')
def index():
    data = get_current_data()
    return render_template('dashboard.html', data=data)

@app.route('/current')
def current():
    data = get_current_data()
    js = json.dumps(data)

    return Response(js, status=200, mimetype='application/json')

@socketio.on('live')
def live_data():
    print 'live'
    data = get_current_data()
    js = json.dumps(data)
    emit('my response', js, broadcast=True)

@socketio.on('connect')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print "Starting Thread"
        thread = LiveThread()
        thread.start()

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



if __name__ == '__main__':
    socketio.run(app)