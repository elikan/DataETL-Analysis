import pandas as pd
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Read in the CSV file into a pandas dataframe
df = pd.read_csv('combined_transactions.csv')

# print(df)

# Split df into purchase and return and drop transaction_type column
purchases_df = df[df['transaction_type'] == 'PurchaseActivity']
returns_df = df[df['transaction_type'] == 'ReturnActivity']
purchases_df.drop(columns='transaction_type', inplace=True)
returns_df.drop(columns='transaction_type', inplace=True)

# print(purchases_df)
# print(returns_df)
# Connect to database
conn = sqlite3.connect('transactions.db')


def create_db():
    # Write purchases and returns to respective tables
    purchases_df.to_sql('purchases', conn)
    returns_df.to_sql('returns', conn)


# create_db()

# Create cursor for SQL queries
cursor = conn.cursor()
purchase_rows = cursor.execute("SELECT * FROM purchases WHERE user_id=? UNION SELECT * FROM returns WHERE user_id=?")
purchases = purchase_rows.fetchall()

# print(purchases)
cursor.close()
conn.close()
cols = [row[0] for row in purchase_rows.description]
df1 = pd.DataFrame(purchases, columns=cols)
print(df1)

if __name__ == '__main__':
    app.run()
