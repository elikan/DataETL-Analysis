import pandas as pd
import sqlite3

# Read in the CSV file into a pandas dataframe
df = pd.read_csv('combined_transactions.csv')

# Convert cents to dollars and drop cents
df['amount_in_dollars'] = round(df['amount_cents'] / 100, 2)
df.drop(columns='amount_cents', inplace=True)

# Split df into purchase and return and drop transaction_type column
purchases_df = df[df['transaction_type'] == 'PurchaseActivity'].copy()
returns_df = df[df['transaction_type'] == 'ReturnActivity'].copy()
purchases_df.drop(columns='transaction_type', inplace=True)
returns_df.drop(columns='transaction_type', inplace=True)

# Connect to database
conn = sqlite3.connect('transactions.db')

# Write purchases and returns to respective tables
purchases_df.to_sql('purchases', conn)
returns_df.to_sql('returns', conn)

# Close connection
conn.close()
