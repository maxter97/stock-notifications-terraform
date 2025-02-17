import os
import json
import urllib.request
import boto3
from datetime import datetime, timezone

def format_stock_data(stock, symbol):
    price = stock.get("05. price", "N/A")
    change = stock.get("09. change", "N/A")
    change_percent = stock.get("10. change percent", "N/A")
    high_52_week = stock.get("03. high", "N/A")
    low_52_week = stock.get("04. low", "N/A")
    timestamp = stock.get("07. latest trading day", "Unknown")
    
    return (
        f"Stock Symbol: {symbol}\n"
        f"Current Price: ${price}\n"
        f"Change: {change}\n"
        f"Change Percent: {change_percent}\n"
        f"52-Week High: ${high_52_week}\n"
        f"52-Week Low: ${low_52_week}\n"
        f"Timestamp: {timestamp}\n"
    )
def get_secret():
    ssm = boto3.client("ssm", region_name="us-east-1")
    response = ssm.get_parameter(Name="stock-api-key", WithDecryption=True)
    return response["Parameter"]["Value"]

def lambda_handler(event, context):
    # Get environment variables
    api_key = get_secret()
    if not api_key:
        return {"statusCode": 500, "body": "API key retrieval failed"}
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")
    
    # Add the stock symbols you want to monitor
    stock_symbols = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB", "NVDA","^GSPC","VOO"] # Example stock symbols
    
    messages = []

    for symbol in stock_symbols:
        # Fetch data from the API
        api_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        try:
            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read().decode())["Global Quote"]
                print(json.dumps(data, indent=4))  # Debugging: log the raw data
                messages.append(format_stock_data(data, symbol))
        except Exception as e:
            print(f"Error fetching data from API for {symbol}: {e}")
            return {"statusCode": 500, "body": "Error fetching data"}
    
    final_message = "\n---\n".join(messages) if messages else "No stock data available."
    
    # Publish to SNS
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="Stock Market Updates"
        )
        print("Message published to SNS successfully.")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}
    
    return {"statusCode": 200, "body": "Data processed and sent to SNS"}