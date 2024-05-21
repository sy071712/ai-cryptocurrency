import pandas as pd
import numpy as np
from datetime import datetime

# Feature calculation functions
def calculate_mid_price(bid_levels, ask_levels):
    return (bid_levels['price'].max() + ask_levels['price'].min()) / 2

def calculate_book_imbalance(bid_levels, ask_levels):
    bid_volume = bid_levels['quantity'].sum()
    ask_volume = ask_levels['quantity'].sum()
    if bid_volume + ask_volume > 0:
        return (bid_volume - ask_volume) / (bid_volume + ask_volume)
    else:
        return float('nan')

def calculate_book_delta(current_mid_price, previous_mid_price):
    if previous_mid_price is not None:
        return current_mid_price - previous_mid_price
    else:
        return 0

# Load order book data
def load_order_book(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# Load trade data
def load_trade_data(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# Select data within a specific time range
def select_time_range(df, start_time, end_time):
    return df[(df['timestamp'] >= start_time) & (df['timestamp'] < end_time)]

# Calculate order book features for each timestamp
def calculate_order_book_features(df):
    features = []
    grouped = df.groupby('timestamp')
    previous_mid_price = None
    for timestamp, group in grouped:
        bid_levels = group[group['type'] == 0]  # Assuming 0 is 'bid'
        ask_levels = group[group['type'] == 1]  # Assuming 1 is 'ask'
        
        mid_price = calculate_mid_price(bid_levels, ask_levels)
        book_imbalance = calculate_book_imbalance(bid_levels, ask_levels)
        book_delta = calculate_book_delta(mid_price, previous_mid_price)
        
        features.append({
            'timestamp': timestamp,
            'mid_price': mid_price,
            'book_imbalance': book_imbalance,
            'book_delta': book_delta
        })
        
        previous_mid_price = mid_price
    
    return pd.DataFrame(features)

# Calculate trade features for each timestamp
def calculate_trade_features(df):
    trade_features = []
    grouped = df.groupby('timestamp')
    for timestamp, group in grouped:
        trade_volume = group['units_traded'].sum()
        number_of_trades = group.shape[0]
        avg_trade_price = group['price'].mean()
        
        trade_features.append({
            'timestamp': timestamp,
            'trade_volume': trade_volume,
            'number_of_trades': number_of_trades,
            'avg_trade_price': avg_trade_price
        })
    
    return pd.DataFrame(trade_features)

# Main function
def main():
    order_book_file = '2024-05-01-upbit-BTC-book.csv'  # Adjust the path as needed
    trade_file = '2024-05-01-upbit-BTC-trade.csv'  # Adjust the path as needed
    
    # Load data
    df_order_book = load_order_book(order_book_file)
    df_trade = load_trade_data(trade_file)
    
    # Select specific 3-hour range
    start_time = '2024-05-01 00:00:00'  # Adjust the start time as needed
    end_time = '2024-05-01 03:00:00'  # 3 hours after the start time
    df_order_book_selected = select_time_range(df_order_book, start_time, end_time)
    df_trade_selected = select_time_range(df_trade, start_time, end_time)
    
    # Calculate features for selected data
    order_book_features_df = calculate_order_book_features(df_order_book_selected)
    trade_features_df = calculate_trade_features(df_trade_selected)
    
    # Merge all features
    final_df = pd.merge(order_book_features_df, trade_features_df, on='timestamp', how='left')
    
    # Select and order columns to match the desired format
    final_df = final_df[['book_delta', 'book_imbalance', 'mid_price', 'timestamp']]
    
    # Save features to CSV
    final_df.to_csv('2024-05-01-upbit-btc-feature.csv', index=False, sep='│')

if __name__ == '__main__':
    main()
