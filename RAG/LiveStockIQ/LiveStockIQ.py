import streamlit as st
import requests
import openai
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key = OPENAI_API_KEY )

# Define Alpha Vantage API endpoint
BASE_URL = "https://www.alphavantage.co/query"

# Company-to-Symbol Mapping
COMPANY_TO_SYMBOL = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Microsoft": "MSFT",
}


# Query Analyzer with Mapping
def query_analyzer_with_mapping(query):
    prompt = f"""
    Classify the following user query into one of three categories:
    1. "Stock Price" if the query is about retrieving the stock price of a company.
    2. "Stock Chart" if the query is about retrieving daily, weekly, or monthly stock charts.
    3. "General Query" if the query is a general knowledge question or unrelated to stock prices or charts.

    If the query is about stock prices or charts, also extract the company name and chart interval if applicable.

    Examples:
    1. "What is the latest stock price of Apple?" -> Category: Stock Price, Company: Apple
    2. "Provide me the daily chart of Tesla." -> Category: Stock Chart, Company: Tesla, Interval: Daily
    3. "Show me the monthly chart for Google." -> Category: Stock Chart, Company: Google, Interval: Monthly
    4. "Tell me about the history of the stock market." -> Category: General Query
    5. "What is the capital of France?" -> Category: General Query

    Query: "{query}"
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
             {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    output = response.choices[0].message.content
    print("LLM Response:", output)  # Debugging statement

    category, company, interval = None, None, None
    try:
        if "Stock Price" in output:
            category = "Stock Price"
            company = output.split("Company:")[-1].split(",")[0].strip() if "Company:" in output else None
        elif "Stock Chart" in output:
            category = "Stock Chart"
            # Extract company and interval properly
            company_part = output.split("Company:")[-1].split("Interval:")[0].strip()
            company = company_part.split(",")[0].strip()
            interval = output.split("Interval:")[-1].strip() if "Interval:" in output else None

        # Map company name to stock symbol
        symbol = COMPANY_TO_SYMBOL.get(company)
        return {"category": category, "company": company, "interval": interval, "symbol": symbol}
    except Exception as e:
        print("Error parsing LLM response:", e)
        return {"category": "General Query", "company": None, "interval": None, "symbol": None}


# Retriever for Stock Price
def retrieve_stock_price(symbol):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        stock_price = data["Global Quote"]["05. price"]
        return stock_price
    except KeyError:
        return "Could not fetch stock price. Please check the stock symbol."


# Retrieve Stock Chart
def retrieve_stock_chart(symbol, interval):
    function = "TIME_SERIES_DAILY" if interval.lower() == "daily" else "TIME_SERIES_WEEKLY" if interval.lower() == "weekly" else "TIME_SERIES_MONTHLY"
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        key = "Time Series (Daily)" if interval.lower() == "daily" else "Weekly Time Series" if interval.lower() == "weekly" else "Monthly Time Series"
        time_series = data[key]
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume",
        })
        df.index = pd.to_datetime(df.index)
        return df.sort_index()
    except KeyError:
        return None


# Generator
def generator(query, context=None):
    prompt = f"""
    You are an AI assistant. Below is some context:
    {context}

    Answer the following query:
    {query}
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content



# Streamlit App
st.title("📈💰 LiveStockIQ 💹💵")
st.write("An innovative application to retrieve real-time stock prices, stock charts, and answer general queries.")

query = st.text_input("Enter your query:")
if st.button("Submit Query"):
    if query:
        analysis = query_analyzer_with_mapping(query)
        print("Analysis:",analysis)
        category = analysis.get("category")
        print("Category", category)
        company = analysis.get("company")
        print("Company", company)
        interval = analysis.get("interval")
        print("Interval", interval)
        symbol = analysis.get("symbol")
        print("Symbol", symbol)

        if category == "Stock Price" and symbol:
            st.subheader("Category: Stock Price")
            st.write(f"Fetching live stock price for {company} ({symbol})...")
            stock_price = retrieve_stock_price(symbol)
            st.write(f"The current stock price of {company} is: ${stock_price}")
        elif category == "Stock Chart" and symbol and interval:
            st.subheader(f"Category: Stock Chart ({interval.capitalize()})")
            st.write(f"Fetching {interval.lower()} chart for {company} ({symbol})...")
            chart_data = retrieve_stock_chart(symbol, interval)
            if chart_data is not None:
                fig = px.line(chart_data, x=chart_data.index, y="Close",
                              title=f"{company} {interval.capitalize()} Stock Prices")
                st.plotly_chart(fig)
            else:
                st.error("Could not fetch stock chart. Please try again.")
        elif category == "General Query":
            st.subheader("Category: General Query")
            st.write("Fetching a response for your query...")
            response = generator(query)
            st.write(response)
        else:
            st.error("Could not determine the category, company, or interval. Please refine your query.")
    else:
        st.warning("Please enter a query.")
