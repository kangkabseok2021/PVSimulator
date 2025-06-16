from rabbitmq import RabbitMQ
import sys
import pandas as pd
import functools
import json
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    print("callback exit")


def main():
    rabbitmq = RabbitMQ()
    try:
        print("Connection to RabbitMQ established successfully.")
        rabbitmq.consume(queue_name="test_queue", callback=callback)
    except Exception as e:
        print(f"Failed to establish connection to RabbitMQ: {e}")
        sys.exit(1)
    finally:
        rabbitmq.close()

def test_TimeDate():
    meters = pd.DataFrame(
        {
            "time": [
                pd.to_datetime("2025-06-13 00:10:10", format='%Y-%m-%d %H:%M:%S'),
                pd.to_datetime("2025-06-13 00:20:00", format='%Y-%m-%d %H:%M:%S'),
                pd.to_datetime("2025-06-13 00:30:00", format='%Y-%m-%d %H:%M:%S'),
            ],
            "MeterA": [13, 33, 12],
            "MeterB": [ 10, 20, 30],
        }
    )
    cTime = pd.to_datetime('2025-06-13 00:00:00', format='%Y-%m-%d %H:%M:%S')
    print(meters['time'][0], cTime.strftime('%Y-%m-%d %H:%M:%S'))
    print(meters['time'][1] - meters['time'][0])
    delta1 = meters['time'][1] - meters['time'][0]
    print(delta1.total_seconds())
    nTime = cTime + pd.Timedelta(seconds = 120)
    print(cTime, nTime)
    meter= {'time': cTime.strftime('%Y-%m-%d %H:%M:%S'), "MeterA": 0, "MeterB": 0}

def ReadingMeterA(stime):
    return stime/10000.0;

def ReadingMeterB(stime):
    x = (stime - 20000.0)/12000;
    if stime < 20000: x = 0.0
    if stime > 68000: x = 4
    return x;

def ReadingMeters(stime):
    ctime = stime + random.randrange(0,300) - 150
    xA = ReadingMeterA(ctime)
    xB = ReadingMeterB(ctime)
    return xA-xB, xB

def generateMeters(outfile):
    ctime = datetime(2025,6,13, 0, 0, 0)
    df = pd.DataFrame(columns=['time', 'MeterA', 'MeterB', 'PowerG'])
    pmB = 0.0
    for i in range(145):
        dtime = ctime + timedelta(seconds=i*600)
        mA, mB = ReadingMeters(i*600);
        #df = df._append({'time': ctime, 'MeterA': mA, 'MeterB': mB}, ignore_index=True)
        df = df._append({'time': dtime, 'MeterA': mA, 'MeterB': mB, 'PowerG': (mB-pmB)*360.0}, ignore_index=True)
        pmB = mB

    print(df)
    df.to_csv(outfile, index=False)
    df.plot(x='time', y = ['MeterA', 'MeterB'])
    plt.savefig("fig_meaterA.png")
    df["Sum"] = df['MeterA'] + df['MeterB']
    df.plot(x='time', y = ['MeterA', 'MeterB', 'Sum', 'PowerG'])
    plt.savefig("fig_meaterB.png")

if __name__ == "__main__":
    test_TimeDate()
    df =pd.DataFrame(columns=['A', 'B'])
    for i in range(5):
        df = df._append({'A': i, 'B': i+2}, ignore_index=True)
    print(df)
    cTime = datetime(2025,6,13, 0, 0, 0) - timedelta(seconds=60)
    dtime = (cTime - datetime(2025,6,13, 0, 0, 0)).total_seconds()
    print(dtime)

   #generateMeters('test1.csv')
