from time import sleep

from azure.cosmos import documents, CosmosClient, exceptions, PartitionKey
from datetime import datetime

import serial
import json
import sys

import config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

client = CosmosClient(url=HOST, credential=MASTER_KEY)
db = client.get_database_client(DATABASE_ID)
container = db.get_container_client(CONTAINER_ID)

def create_items(container, json_data):
    container.create_item(body=json_data)
    
def modify_json(json_data):
    now = datetime.now()
    data = json.loads(json_data)
    
    new_id = data["id"] + "-{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}" .format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    
    items = {
        'id': new_id,
        'deviceID': data["deviceID"],
        't': data["t"],
        'h': data["h"],
        'l': data["l"],
        's': data["s"],
        'w': data["w"],
        'date': str(now)
    }
    
    print(items)

    create_items(container, items)

ser1 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
ser3 = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)

while True:
    try:
        if ser1.in_waiting > 0:
            try:
                data = ser1.readline().decode('utf-8').rstrip()
                modify_json(data)
                ser1.reset_input_buffer()
            except json.JSONDecodeError as e:
                print(e)
        
        if ser2.in_waiting > 0:
            try:
                data = ser2.readline().decode('utf-8').rstrip()
                modify_json(data)
                ser2.reset_input_buffer()
            except json.JSONDecodeError as e:
                print(e)
            
        if ser3.in_waiting > 0:
            try:
                data = ser3.readline().decode('utf-8').rstrip()
                modify_json(data)
                ser3.reset_input_buffer()
            except json.JSONDecodeError as e:
                print(e)
            
        sleep(1)
    except exceptions.CosmosHttpResponseError as e:
        print(e)
        print("Reconnecting to the database in 3 seconds...")
        sleep(3)
        client = CosmosClient(url=HOST, credential=MASTER_KEY)
        db = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)

