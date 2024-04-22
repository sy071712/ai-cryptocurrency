import time
import urllib.request
import pandas as pd
import datetime
import json
import os.path

previous_date = None
current_file = None

while True:
    current_time = datetime.datetime.now()
    current_date = current_time.strftime("%Y-%m-%d")
    current_hour = current_time.strftime("%H-%M-%S")

    if current_date != previous_date:
        current_file = f"./book-{current_date}-bithumb-BTC.csv"
        os.makedirs(os.path.dirname(current_file), exist_ok=True)
        previous_date = current_date

    if current_time.hour == 0 and current_time.minute == 0 and current_time.second <= 5:
        current_file = f"./book-{current_date}-bithumb-BTC.csv"
        os.makedirs(os.path.dirname(current_file), exist_ok=True)

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

    df.to_csv(current_file, index=False, mode='a', header=not os.path.exists(current_file), sep='|')

    time.sleep(4.9)

