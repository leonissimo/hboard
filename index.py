from sense_hat import SenseHat
from datetime import datetime
from elasticsearch import Elasticsearch
import time

sense = SenseHat()
es = Elasticsearch(['http://192.168.0.21:9200'])

def get_current_data():
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()
    tp = sense.get_temperature_from_pressure()
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'temperature':str(round(t, 1)),
        'pressure':str(round(p,1)),
        'humidity':str(round(h,1)),
        'temperatureP':str(round(tp,1)),
        'datetime' : dt
    }
    return data

def index_data():
    data = get_current_data()
    res = es.index(index="hm", doc_type='hm', body=data)

def index_every(secs):
    while True:
        print 'indexing'
        try:
            index_data()
        except:
            time.sleep(60*10) #wait 10 mins
            continue
        time.sleep(secs)


if __name__ == '__main__':
    index_every(60*2)