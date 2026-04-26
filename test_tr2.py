import pandas as pd

df = pd.read_csv('data/2026-04-26-traderepublic-export.csv')
df = df[df['status'] == 'executed'].copy()
df['subtitle'] = df['subtitle'].fillna('')

print("All positive values without 'Erik Pillon' or 'Interest/Dividend' or 'Sell Order':")
others = df[(df['value'] > 0) & (~df['title'].str.contains('Erik Pillon|PILLON ERIK', case=False, na=False)) & (~df['subtitle'].str.contains('Cash dividend|Interest|Fixed Interest|Bonus|Sell Order', case=False, na=False)) & (~df['title'].str.contains('Interest', case=False, na=False))]
print(others[['title', 'subtitle', 'value']])
