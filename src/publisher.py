from rabbitmq import RabbitMQ
import pandas as pd
import json
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def ReadingMeterA(stime):
    return stime/10000.0;

def ReadingMeterB(stime):
    x = (stime - 20000.0)/12000;
    if stime < 20000: x = 0.0
    if stime > 68000: x = 4
    return x;

def ReadingMeters(stime):
    ctime = stime + random.randrange(0,200) - 100
    xA = ReadingMeterA(ctime)
    xB = ReadingMeterB(ctime)
    return xA-xB, xB

class Publisher:
    def __init__(self, mqueue, start_time, end_time, delta_time):
        self.mqueue = mqueue
        self.stime = start_time
        self.etime = end_time
        self.deltat = delta_time

    def publish(self):
        rabbitmq = RabbitMQ()
        #print(start_time)
        meter= {'time': self.stime, "MeterA": 0.0, "MeterB": 0.0}
        json_meter = json.dumps(meter, default=serialize_datetime)
        rabbitmq.publish(queue_name=self.mqueue, message=json_meter)
        cTime = self.stime
        dtime = (self.stime - datetime(2025,6,13, 0, 0, 0)).total_seconds()
        ddtime = int(dtime)
        while cTime < self.etime+timedelta(seconds=self.deltat):
            cTime += timedelta(seconds=self.deltat)
            ddtime += self.deltat
            mA, mB = ReadingMeters(ddtime)
            message = {'time': cTime, 'MeterA': mA, 'MeterB': mB}
            json_message = json.dumps(message, default=serialize_datetime)
            # print(message, json_message)
            rabbitmq.publish(queue_name=self.mqueue, message=json_message)

        print("Meters published successfully.")
        rabbitmq.close();
    

    def publish_messages(messages):
        rabbitmq = RabbitMQ()
        cTime = datetime(2025,6,13, 0, 0, 0)
        print(cTime, cTime.strftime('%Y-%m-%d %H:%M:%S'))
        meter= {'time': cTime.strftime('%Y-%m-%d %H:%M:%S'), "MeterA": 0, "MeterB": 0}
        json_meter = json.dumps(meter)
        rabbitmq.publish(queue_name=meter_queue, message=json_meter)
        messages = meters.to_dict('records')
        # print(messages)
        for message in messages:
            json_message = json.dumps(message, default=serialize_datetime)
            #print(message, json.dumps(message))
            rabbitmq.publish(queue_name=meter_queue, message=json_message)
        # rabbitmq.publish(queue_name=meter_queue, message=str(messages))
        print("Meters published successfully.")
        rabbitmq.close();

def publish_test_message():
    rabbitmq = RabbitMQ()
    try:
        rabbitmq.publish(queue_name="test_queue", message="Test message")
        print("Test message published successfully.")
    except Exception as e:
        print(f"Failed to publish test message: {e}")
    finally:
        rabbitmq.close()


if __name__ == "__main__":
    cTime = datetime(2025,6,13, 0, 0, 0) - timedelta(seconds=60)
    publish_meter = Publisher("meter_queue", cTime, datetime(2025,6,14, 0, 0, 0), 600)
    publish_meter.publish()

    #publish_test_message()
    meters = pd.DataFrame(
        {
            "time": [
                datetime(2025,6,13, 0, 10, 0),
                datetime(2025,6,13, 0, 20, 0),
                datetime(2025,6,13, 0, 30, 0),
            ],
            "MeterA": [13.0, 23.0, 32.0],
            "MeterB": [10.0, 20.0, 30.0],
        }
    )
    #publish_messages("meter_queue", meters)

