import pandas as pd
import yfinance as yf

df = pd.read_csv('data/2026-04-26-traderepublic-export.csv')
df = df[df['status'] == 'executed'].copy()

# Handle NaNs in subtitle
df['subtitle'] = df['subtitle'].fillna('')

df['category'] = 'Expenses' # default
df.loc[df['title'].str.contains('Erik Pillon|PILLON ERIK', case=False, na=False), 'category'] = 'Deposits/Withdrawals'
df.loc[df['subtitle'].str.contains('Saving executed|Buy Order|Sell Order', case=False, na=False), 'category'] = 'Investments'
df.loc[df['subtitle'].str.contains('Cash dividend|Interest payment|Fixed Interest|Bonus', case=False, na=False) | df['title'].str.contains('Interest', case=False, na=False), 'category'] = 'Dividends/Interests'

print("Value by Category:")
print(df.groupby('category')['value'].sum())
print("\nTransactions in Expenses:")
print(df[df['category'] == 'Expenses']['title'].unique())
