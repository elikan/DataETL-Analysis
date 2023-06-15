import pandas as pd
import numpy as np
import statsmodels.api as sm

df0 = pd.read_csv('combined_transactions.csv', usecols=['amount_cents', 'datetime', 'merchant_type_code'])

# Find where merchant_type_code is 5732 and put in data df
df = df0[df0['merchant_type_code'] == 5732].copy()

# No longer need merchant_type_code, so drop it
df.drop(columns='merchant_type_code', inplace=True)

df['amount_in_dollars'] = round(df['amount_cents'] / 100, 2)
df.drop(columns='amount_cents', inplace=True)


# Convert the datetime column to year-month-day format and drop datetime
df['date'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d')
df.drop(columns='datetime', inplace=True)

# Set  date as the index and sort it
df.set_index('date', inplace=True)
df.sort_index(ascending=True, inplace=True)

# Get total amount for each day
df_daily = df.resample('D').sum()

# Create model and fit it
model = sm.tsa.ARIMA(df_daily['amount_in_dollars'], order=(2, 1, 1))
results = model.fit()

# Forecast the next 10 days
forecast = results.forecast(steps=10)

# Put forcat to  df and renamed co amount_in_dollars
df1 = forecast.to_frame()
df1 = df1.rename(columns={'predicted_mean': 'amount_in_dollars'})
df1['amount_in_dollars'] = df1['amount_in_dollars'].round(2)

print(df1)
