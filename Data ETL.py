import pandas as pd
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Read in the CSV file into a pandas dataframe
df = pd.read_csv('combined_transactions.csv')

df['amount_in_dollars'] = df['amount_cents'] / 100
df.drop(columns='amount_cents', inplace=True)

# Split df into purchase and return and drop transaction_type column
purchases_df = df[df['transaction_type'] == 'PurchaseActivity'].copy()
returns_df = df[df['transaction_type'] == 'ReturnActivity'].copy()
# purchases_df.drop(columns='transaction_type', inplace=True)
# returns_df.drop(columns='transaction_type', inplace=True)

# print(purchases_df)
# print(returns_df)
# Connect to database
conn = sqlite3.connect('transactions.db')


def create_db():
    # Write purchases and returns to respective tables
    purchases_df.to_sql('purchases', conn)
    returns_df.to_sql('returns', conn)


create_db()


# Create cursor for SQL queries

# purchase_rows = cursor.execute(
#     "SELECT * FROM purchases WHERE user_id=333 UNION SELECT * FROM returns WHERE user_id=333")
# global purchases
# purchases = purchase_rows.fetchall()


@app.route('/<int:num>', methods=['GET'])
def get_transactions(num):
    conn = sqlite3.connect('transactions.db')
    print(num)
    cursor = conn.cursor()
    query = "SELECT * FROM purchases WHERE user_id=? "

    cursor.execute(
        "SELECT user_id, amount_in_dollars, datetime, merchant_type_code, transaction_type FROM purchases WHERE user_id=? UNION SELECT user_id, amount_in_dollars, datetime, merchant_type_code, transaction_type FROM returns WHERE user_id=?",
        (num, num,))
    purchases = cursor.fetchall()
    conn.close()

    transactions = []
    for row in purchases:
        transaction = {
            'user_id': row[0],
            'amount_in_dollars': row[1],
            'datetime': row[2],
            'merchant_type_code': row[3],
            'transaction_type': row[4]
        }
        transactions.append(transaction)

    response = {'transactions': transactions}
    return jsonify(response)


# print(purchases)

# cols = [row[0] for row in purchase_rows.description]
# df1 = pd.DataFrame(purchases, columns=cols)
# print(df1)

if __name__ == '__main__':
    app.run()
