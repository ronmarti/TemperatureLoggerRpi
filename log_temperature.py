#! /usr/bin/python3
import pygsheets
from datetime import datetime, timezone
from bmp180_reader import read_sensor
import json
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


cTemp, pressure, altitude = read_sensor()

try:
    #authorization
    gc = pygsheets.authorize(service_file='.secrets/temperaturelogger-337216-d93f88657a6b.json')

    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('LogTeploty')

    #select the first sheet 
    wks = sh[0]

    now = datetime.today().strftime('%d.%m.%Y %H:%M:%S')
    wks.append_table([now, cTemp, pressure])
    wks.update_value('D2', now)
    wks.update_value('E2', cTemp)
except Exception as exc:
    print(exc)

try:
    with open('.secrets/influxsecrets.json',) as influxsecrets:
        config = json.load(influxsecrets)
        influx_token = config['token']
        influx_address = config['address']
        org = config['org']
        bucket = config['bucket']

        with InfluxDBClient(url=influx_address, token=influx_token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            now = round(1e9*datetime.now(timezone.utc).timestamp())
            write_api.write(bucket, org,f"rpi temperature={cTemp} {now}")
            write_api.write(bucket, org,f"rpi pressure={pressure} {now}")
except Exception as exc:
    print(exc)
