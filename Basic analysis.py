import pandas as pd
import numpy as np
import statsmodels.api as sm

df1 = pd.read_csv('combined_transactions.csv', usecols=['amount_cents', 'datetime', 'merchant_type_code'])

# Find where merchant_type_code is 5732 and put in data df
df = df1[df1['merchant_type_code'] == 5732].copy()

# No longer need merchant_type_code, so drop it
df.drop(columns='merchant_type_code', inplace=True)

# data['amount_in_dollars'] = round(data['amount_cents'] / 100, 2)
# data.drop(columns='amount_cents', inplace=True)


# Convert the datetime column to date format
df['date'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d')
df.drop(columns='datetime', inplace=True)
# Set the date column as the index
df.set_index('date', inplace=True)

# Sort the DataFrame based on the index in ascending order
df.sort_index(ascending=True, inplace=True)

# Resample the DataFrame to daily frequency and sum the 'amount_cents' column
df_daily = df.resample('D').sum()

# Create a time series model
model = sm.tsa.ARIMA(df_daily['amount_cents'], order=(2, 1, 1))

# Fit the model to the data
results = model.fit()

# Forecast the next 10 days
forecast = results.forecast(steps=10)

print(forecast)


