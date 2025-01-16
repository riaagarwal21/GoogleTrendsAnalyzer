import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

# Initialize pytrends request
trendingTopics = TrendReq(hl='en-US', tz=360)

# Create a directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Define a function to fetch and display interest over time
def fetch_interest_over_time(keywords, timeframe, top_n=10, output_file=None):
    trendingTopics.build_payload(keywords, cat=0, timeframe=timeframe)
    time.sleep(5)  # Prevent rate-limiting
    data = trendingTopics.interest_over_time()
    if not data.empty:
        data = data.sort_values(by=keywords[0], ascending=False).head(top_n)
        print(f"Top {top_n} records for interest over time:")
        print(data)
        if output_file:
            data.to_csv(output_file)
            print(f"Data saved to {output_file}")
    else:
        print("No data available for the given timeframe.")
    return data

# Define a function to fetch and display interest by region
def fetch_interest_by_region(keywords, top_n=10, output_file=None):
    trendingTopics.build_payload(keywords, cat=0)
    data = trendingTopics.interest_by_region()
    if not data.empty:
        data = data.sort_values(by=keywords[0], ascending=False).head(top_n)
        print(f"Top {top_n} regions for interest by topic:")
        print(data)
        # Plot interest by region
        data.reset_index().plot(x='geoName', y=keywords[0], figsize=(10, 5), kind='bar')
        plt.title(f"Top {top_n} Regions for {keywords[0]}")
        plt.xlabel("Region")
        plt.ylabel("Interest")
        plt.style.use('fivethirtyeight')
        plt.show()
        if output_file:
            data.to_csv(output_file)
            print(f"Data saved to {output_file}")
    else:
        print("No data available for regions.")
    return data

# Main execution block
def main():
    # Define the list of keywords
    keywordsList = ["AI"]

    print("Fetching interest over the past year...")
    yearly_interest = fetch_interest_over_time(
        keywordsList, timeframe='today 12-m', output_file="data/yearly_interest.csv"
    )

    print("Fetching historical hourly interest...")
    hourly_interest = fetch_interest_over_time(
        keywordsList, timeframe='2024-12-15 2025-01-15', output_file="data/hourly_interest.csv"
    )

    print("Fetching interest by region...")
    regional_interest = fetch_interest_by_region(
        keywordsList, output_file="data/regional_interest.csv"
    )

    print("Analysis complete.")

if __name__ == "__main__":
    main()
