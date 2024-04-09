import time
import urllib.request
import pandas as pd
import datetime
import json

while True:
    book = {}
    response = urllib.request.urlopen('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    data = response.read().decode('utf-8')
    book = json.loads(data)

    data = book['data']

    bids_df = pd.DataFrame(data['bids'])
    bids_df = bids_df.apply(pd.to_numeric, errors='coerce')
    bids_df.dropna(inplace=True)
    bids_df.sort_values('price', ascending=False, inplace=True)
    bids_df['type'] = 0

    asks_df = pd.DataFrame(data['asks'])
    asks_df = asks_df.apply(pd.to_numeric, errors='coerce')
    asks_df.dropna(inplace=True)
    asks_df.sort_values('price', ascending=True, inplace=True)
    asks_df['type'] = 1

    df = pd.concat([bids_df, asks_df], ignore_index=True)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = timestamp

    with open("./2022-05-18-bithumb-orderbook.csv", "a") as f:
        df.to_csv(f, index=False, header=False, mode='a')

    time.sleep(4.9)


   



