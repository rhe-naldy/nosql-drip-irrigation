from azure.cosmos import CosmosClient
import pandas as pd
from datetime import datetime

import config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

def download_csv(client):
    db = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    query = "SELECT * FROM c" 
    items = list(container.query_items(query, enable_cross_partition_query=True))

    df = pd.DataFrame(items)
    now = datetime.now()
    string = 'data-{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}' .format(now.year, now.month, now.day, now.hour, now.minute, now.second) + '.csv'
    df.to_csv(string , index=False)


def run_sample():
    client = CosmosClient(url=HOST, credential=MASTER_KEY)

    download_csv(client)

if __name__ == '__main__':
    run_sample()
