import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("ai-crypto-project-3-live-btc-krw.csv")

data['TradeValue'] = data['quantity'] * data['price']
data['NetAmount'] = data.apply(lambda row: -row['amount'] if row['side'] == 0 else row['amount'], axis=1)
data['PnL'] = data['NetAmount'] - data['fee']

data['CumulativePnL'] = data['PnL'].cumsum()

print(data[['timestamp', 'quantity', 'price', 'fee', 'amount', 'side', 'PnL', 'CumulativePnL']])

data.to_csv("PnL_results.csv", index=False)

plt.figure(figsize=(10, 6))
plt.plot(data['timestamp'], data['CumulativePnL'], label='Cumulative PnL')
plt.xlabel('Timestamp')
plt.ylabel('PnL')
plt.title('Cumulative PnL Over Time')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

