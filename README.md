# Stock Notification System 
Project 2 for DevOp Challenge #DevOpsAllStarsChallenge
## Overview
Creating a stock notification system to send real-time data on your favorte stocks to users thought email and/or text.

<img width="853" alt="Screenshot 2025-01-13 at 11 19 16 AM" src="https://github.com/user-attachments/assets/97457744-d683-463b-87ea-fa2a9b1ae5c6" />

## Prerequisites
1. Familiar with AWS and Python
2. An AWS Account 
3. API Key from Alpha Vantage or any stock market API
4. A Code/Text Editor: To edit any code if needed
## Instruction
### 1. Obtian an API key from Alpha Vantage
Sign up at https://www.alphavantage.co/support/#api-key for a free tier key.
Make sure to save the key for later in the project
### 2. Create a AWS SNS Topic
Selcet Standard for type and name(ex.stock_topic) your topic. Then hit create Topic. Save the ARN for the topic to use for later
### 3. Create SNS Policy and role for Lambda 
In the poicy editor select JSON and input this code.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:REGION:ACCOUNT_ID:stock_topic"
        }
    ]
}
```
* Replace "arn:aws:sns:REGION:ACCOUNT_ID:stock_topic" with ARN from the SNS topic.

### 4. Use newly created policy to create a role 
The policy willl be used to give permistions to a role. That will be attached to the lambda function that will be used later in the project.
Here is the policy: 
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:REGION:ACCOUNT_ID:stock_topic"
        }
    ]
}
```
![image](https://github.com/user-attachments/assets/22be914a-e454-4988-be37-f6ed62b03aec)

### 5. Create Lambda function
Create a new Lambda function. Choose python 3.xx as the runtime and x86_64 as the architecture. Attach the newly created role to it.
![Screenshot 2025-01-12 164536](https://github.com/user-attachments/assets/bf1db415-47ca-4ce1-84bd-dd1403129bce)


### 6. Create subscription for SNS topic and subscribe to it
You can subscribe using email and/or SMS
![Screenshot 2025-01-12 163149](https://github.com/user-attachments/assets/fa33d1e1-fef5-423d-bc2f-f363de3c9ca6)
![Screenshot 2025-01-12 163157](https://github.com/user-attachments/assets/74ac425b-243e-4e27-8f8c-e8118dd726d9)
Then you will recieve a message and have to confirm 

![Screenshot 2025-01-12 163426](https://github.com/user-attachments/assets/d346edba-28f4-457e-92d5-ada91ad02d9e)


### 7. Add code and Environment Variables to Lambda function
Insert code from stock_notifications.py and put it inside the lambda function.

Here is the code:
```
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

def lambda_handler(event, context):
    # Get environment variables
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")
    
    # Add the stock symbols you want to monitor
    stock_symbols = ["AAPL", "GOOGL", "AMZN"]
    
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
```
(If you want to test using different stocks make changes to this line of code with the symbol of the stocks you want to see)
![image](https://github.com/user-attachments/assets/10cb0fee-26dd-4f0a-8a4a-c8d42cb06e55)

Add Environment Variables so it can be used by the code.
![image](https://github.com/user-attachments/assets/e6898fd9-0b61-433f-890f-cf340e2a12e5)

### 8. Test and Deploy Code 
Deploy the code. After test the code . (If any error occur try changing the timeout for the function from 3s to 6s or more.)
![image](https://github.com/user-attachments/assets/3e0be380-a667-47f0-9929-d6dd01da63cd)

Here is what a succesful test looks like:


![image](https://github.com/user-attachments/assets/b5b219df-11a3-485c-9273-eb1d93543e28)




### (Optional) Configure EventBridge Schedule to receive Notifcations at a certain period of time
![Screenshot 2025-01-12 171738](https://github.com/user-attachments/assets/bdbbd72b-6d4c-432c-be2e-3361abd187c0)


## What was learned 
- Create an SNS topic for users to subscribe too
- Setting up SNS to send messaseges 
- Create a Lambda function
- Using code and environment varialbes inside an Lambda fuction 
- Adding policys and roles to Lambda 
- Retirving data from an api and changing it to a readable format
- Tesing before delpoying your code 
## Future Improvements
- Have a link users and click to subsribe 
- Have a way to enter what stocks they want to see outside of changing the code inside the fuction 
