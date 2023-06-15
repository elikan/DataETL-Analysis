import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Transactions(Resource):
    def get(self, num):
        # Connect to database
        conn = sqlite3.connect('transactions.db')
        # Create cursor for SQL queries
        cursor = conn.cursor()
        # SQL query to get user_id, amount_in_dollars, datetime, merchant_type_code, transaction_type for given user_id
        cursor.execute('''
        SELECT user_id, amount_in_dollars, datetime, merchant_type_code FROM purchases WHERE user_id=? 
        UNION ALL
        SELECT user_id, amount_in_dollars, datetime, merchant_type_code FROM returns WHERE user_id=?
        ''', (num, num,))
        # Fetch query results
        rows = cursor.fetchall()

        # Close connection
        conn.close()

        # For each row in query results out into dictionary to convert into JSON
        transactions = []
        for row in rows:
            transaction = {
                'user_id': row[0],
                'amount_in_dollars': row[1],
                'datetime': row[2],
                'merchant_type_code': row[3],
            }
            transactions.append(transaction)

        response = {'transactions': transactions}
        # Convert to JSON
        return jsonify(response)


class Profit(Resource):
    def get(self, num):
        # Connect to database
        conn = sqlite3.connect('transactions.db')
        # Create cursor for SQL queries
        cursor = conn.cursor()
        # SQL query to get merchant_type_code and find profit for that merchant
        cursor.execute('''
        SELECT p.merchant_type_code, round((p.total_amount - COALESCE(r.total_amount, 0)),2) AS net_amount_in_dollars
        FROM(
        SELECT merchant_type_code, sum(amount_in_dollars) AS total_amount FROM purchases WHERE merchant_type_code=?) AS p
        JOIN(
        SELECT merchant_type_code, sum(amount_in_dollars) AS total_amount FROM returns WHERE merchant_type_code=?) AS r
        ''', (num, num,))

        # Fetch query results
        rows = cursor.fetchall()

        # SQL query to get datetime and convert to date for that merchant
        cursor.execute('''
              SELECT strftime('%Y-%m-%d', datetime) as date from purchases where merchant_type_code = ? 
              UNION ALL SELECT strftime('%Y-%m-%d', datetime) as date from returns where merchant_type_code = ?
              ''', (num, num,))
        # Fetch query results
        rows2 = cursor.fetchall()

        # Close connection
        conn.close()

        # put merchant values in a dictionary to be converted into JSON
        merchants = []
        for row in rows:
            merchant = {
                'merchant_type_code': row[0],
                'net_amount_in_dollars': row[1],
                'date': rows2
            }
            merchants.append(merchant)
        response = {'merchant': merchants}
        # Convert to JSON
        return jsonify(response)

# Endpoint for all transactions of a user
api.add_resource(Transactions, '/user/<int:num>')
# Endpoint for total profit of a merchant
api.add_resource(Profit, '/profit/<int:num>')

if __name__ == '__main__':
    app.run()
