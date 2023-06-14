import pandas as pd

df = pd.read_csv('combined_transactions.csv')
df1 = df[df['merchant_type_code'] == 5732]
print(df1)