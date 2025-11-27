# Start your code here!
import os
import pandas as pd
from openai import OpenAI

# Instantiate an API client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Read in the two datasets
nasdaq100_ca = pd.read_csv("nasdaq100_CA.csv")
price_change = pd.read_csv("nasdaq100_price_change.csv")

# Merge YTD performance into nasdaq100_ca
nasdaq100_ca = nasdaq100_ca.merge(price_change[["symbol", "ytd"]], on="symbol", how="inner")

# Preview the combined dataset
print(nasdaq100_ca.head())

# Loop through each NASDAQ company to classify its sector
for company in nasdaq100_ca["symbol"]:
    prompt = f"""
Classify the company {company} into one of the following sectors. 
Answer only with the sector name: Technology, Consumer Cyclical, Industrials, Utilities, Healthcare, Communication, Energy, Consumer Defensive, Real Estate, Financial.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    sector = response.choices[0].message.content.strip()  # remove whitespace
    nasdaq100_ca.loc[nasdaq100_ca["symbol"] == company, "sector"] = sector

# Show sector distribution
print(nasdaq100_ca["sector"].value_counts())

# Prepare a concise prompt for stock recommendations
company_data = nasdaq100_ca[["symbol","name","ytd","sector"]].to_dict(orient="records")
prompt_recommendation = f"""
Based on the following California Nasdaq-100 companies and their YTD performance, recommend the two best sectors and at least two companies per sector. Return only sector names and companies:

{company_data}
"""

# Get the model response
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt_recommendation}],
    temperature=0.0
)

# Store the recommendations
stock_recommendations = response.choices[0].message.content
print(stock_recommendations)
