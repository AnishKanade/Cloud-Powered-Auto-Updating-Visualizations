import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta
import boto3
import os
# add your private api key

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
s3 = boto3.resource('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


# List of bank tickers
tickers = ['JPM', 'BAC', 'C', 'WFC', 'GS']

# Dictionary to store DataFrames for each ticker
data_dict = {}

# Define the start date for a 5-year lookback
end_date = datetime.today()
start_date = end_date - timedelta(days=5 * 365)

for ticker in tickers:
    # Construct the API URL for daily stock prices
    url = f'https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=5000&apikey={TWELVE_DATA_API_KEY}'
    
    # Fetch the data
    response = requests.get(url)
    
    # Check if the API request was successful
    if response.status_code != 200:
        print(f"Error fetching data for {ticker}: HTTP {response.status_code}")
        continue

    try:
        data = response.json()
    except ValueError:
        print(f"Error decoding JSON for {ticker}")
        continue

    # Print a preview of the API response (limit output for readability)
    print(f"Response sample for {ticker}: {str(data)[:500]}...\n")  # Limit to 500 chars

    # Check if the response contains valid data
    if "values" in data and isinstance(data["values"], list):
        ts_data = data["values"]

        # Create a DataFrame from the JSON data
        df = pd.DataFrame(ts_data)

        # Ensure datetime conversion and set index
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        df.set_index('datetime', inplace=True)

        # Convert closing price to float
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df = df[['close']].rename(columns={'close': ticker})

        # Drop any rows with missing values
        df.dropna(inplace=True)

        # Ensure data is sorted before filtering
        df.sort_index(inplace=True)

        # Filter for the last 5 years
        df = df.loc[start_date:end_date]

        # Store the DataFrame in our dictionary
        if not df.empty:
            data_dict[ticker] = df
        else:
            print(f"No data available for {ticker} in the last 5 years.")
    else:
        print(f"Invalid data format for {ticker}: {data}")

# Merge all the individual DataFrames on their dates
if data_dict:
    bank_data = pd.concat(data_dict.values(), axis=1, join='inner')
    print("\nMerged DataFrame Preview:")
    print(bank_data.head())
else:
    print("No valid data was collected.")


# Plot stock prices over time
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(bank_data.index, bank_data[ticker], label=ticker)

plt.xlabel("Date")
plt.ylabel("Stock Price (USD)")
plt.title("Stock Prices of Major Banks Over the Last 5 Years")
plt.legend()
plt.grid(True)
plt.show()

# Set the size of the canvas
plt.figure(figsize=(18,12))

# Create a boxplot of the transposed data (so each box represents one bank)
plt.boxplot(bank_data.transpose())

# Add chart and axis titles
plt.title('Boxplot of Bank Stock Prices (5Y Lookback)', fontsize=20)
plt.xlabel('Bank', fontsize=20)
plt.ylabel('Stock Prices', fontsize=20)

# Set the x-axis labels
ticks = range(1, len(bank_data.columns)+1)
labels = list(bank_data.columns)
plt.xticks(ticks, labels, fontsize=20)

# Save the plot to a file
plt.savefig('bank_data_boxplot.png')
plt.show()

################################################
# Pushes the file to the AWS S3 bucket
s3 = boto3.resource('s3')
s3.meta.client.upload_file('bank_data_boxplot.png', 'anish-aws-bucket', 'bank_data_boxplot.png')
print("File uploaded to S3 successfully.")
