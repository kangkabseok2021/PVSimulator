from rabbitmq import RabbitMQ
import sys
import pandas as pd
import functools
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


class Consumer:
    def __init__(self, mqueue, start_time, end_time, delta_time, outfile):
        self.mqueue = mqueue
        self.outfile = outfile
        self.start_time = start_time
        self.delta = delta_time
        self.end_time = end_time
        self.pMeter = {'time': datetime(2025,6,13, 0, 0, 0), 'MeterA': 0.0, 'MeterB': 0.0}
        self.last_time = datetime(2025,6,13, 0, 0, 0)

    def append_Meters(self, after_Meter):
        #df = pd.DataFrame(columns=['time', 'MeterA', 'MeterB', 'Sum', 'PowerG'])
        dsecond = (after_Meter['time'] - self.pMeter['time']).total_seconds()
        #print(dsecond, self.delta)
        dA = after_Meter['MeterA'] - self.pMeter['MeterA']
        dB = after_Meter['MeterB'] - self.pMeter['MeterB']
        cTime = self.last_time + timedelta(seconds=self.delta)
        msecond =  (cTime - self.pMeter['time']).total_seconds()
        pB = dB/dsecond
        pA = dA/dsecond
        df_exist = False
        while cTime <= self.end_time and msecond <= dsecond:
            mA = self.pMeter['MeterA'] + pA * msecond
            mB = self.pMeter['MeterB'] + pB * msecond
            if df_exist: 
                df = df._append({'time': cTime, 'MeterA': mA, 'MeterB': mB, 'Sum': mA+mB,'PowerG': pB*36000}, ignore_index=True)
            else: 
                df = pd.DataFrame({'time': [cTime], 'MeterA': [mA], 'MeterB': [mB], 'Sum': [mA+mB],'PowerG': [pB*36000]},
                                    columns=['time', 'MeterA', 'MeterB', 'Sum', 'PowerG'])
                df_exist = True
            msecond += self.delta
            if msecond <= dsecond: 
                cTime += timedelta(seconds=self.delta)
        self.last_time = cTime
        if cTime + timedelta(seconds=self.delta) > self.end_time:
            msecond =  (self.end_time - self.pMeter['time']).total_seconds()
            mA = self.pMeter['MeterA'] + pA * msecond
            mB = self.pMeter['MeterB'] + pB * msecond
            if df_exist: 
                df = df._append({'time': cTime, 'MeterA': mA, 'MeterB': mB, 'Sum': mA+mB,'PowerG': pB*36000}, ignore_index=True)
            else: 
                df = pd.DataFrame({'time': [cTime], 'MeterA': [mA], 'MeterB': [mB], 'Sum': [mA+mB],'PowerG': [pB*36000]},
                                    columns=['time', 'MeterA', 'MeterB', 'Sum', 'PowerG'])
                df_exist = True
            self.last_time = self.end_time
        #print(df)

        df.to_csv(outfile, mode='a', index=False, header=False)
        if self.last_time == self.end_time:
            ddf = pd.read_csv(outfile)
            print(ddf)
            ddf.plot(x='time', y = ['MeterA', 'MeterB', 'Sum', 'PowerG'])
            plt.gcf().autofmt_xdate()
            plt.savefig("./Images/fig_power.png")


    def call_consume(self, ch, method, properties, body):
        after_Meter = json.loads(body.decode('utf-8'))
        after_Meter['time'] = pd.to_datetime(after_Meter['time'], format='mixed')
        if after_Meter['time'] > self.start_time and self.pMeter['time'] < self.end_time:
            self.append_Meters(after_Meter)
        else:
            print(after_Meter['time'])
            df = pd.DataFrame(columns=['time', 'MeterA', 'MeterB', 'Sum', 'PowerG'])
            df.to_csv(outfile, index=False)
        self.pMeter = after_Meter.copy()

    def consumer(self):
        rabbitmq = RabbitMQ()
        try:
            print("Connection to RabbitMQ established successfully.")
            rabbitmq.consume(queue_name=self.mqueue, callback=self.call_consume)
        except Exception as e:
            print(f"Failed to establish connection to RabbitMQ: {e}")
            sys.exit(1)
        finally:
            rabbitmq.close()

def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    print("callback exit")


def test_consumer():
    rabbitmq = RabbitMQ()
    try:
        print("Connection to RabbitMQ established successfully.")
        rabbitmq.consume(queue_name="test_queue", callback=callback)
    except Exception as e:
        print(f"Failed to establish connection to RabbitMQ: {e}")
        sys.exit(1)
    finally:
        rabbitmq.close()


if __name__ == "__main__":
    start_time = datetime(2025,6,13, 0, 0, 0)
    cTime = start_time - timedelta(seconds=60)
    end_time = datetime(2025,6,14, 0, 0, 0)
    outfile = "./Images/power.csv"
    consumer_m = Consumer("meter_queue", start_time, end_time, 60, outfile)
    consumer_m.consumer()

