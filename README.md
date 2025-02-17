# Stock Notification System 
Updated Version of previous project https://github.com/maxter97/stock-notifications 
## Overview
Creating a stock notification system to send real-time data on your favorte stocks to users thought email and/or text. Now using terraform!

<img width="853" alt="Screenshot 2025-01-13 at 11 19 16 AM" src="https://github.com/user-attachments/assets/97457744-d683-463b-87ea-fa2a9b1ae5c6" />

## Prerequisites
1. Familiar with AWS and Python
2. An AWS Account 
3. API Key from Alpha Vantage or any stock market API
4. A Code/Text Editor: To edit any code if needed
5. Terraform 
## Instruction
*To add/remove the stocks you receive make changes to this line of code with the symbol of the stocks you want to see in the stock-notifications.py file
</br>
![image](https://github.com/user-attachments/assets/10cb0fee-26dd-4f0a-8a4a-c8d42cb06e55)
### 1. Obtain an API key from Alpha Vantage
Sign up at https://www.alphavantage.co/support/#api-key for a free tier key.
Make sure to save the key for later in the project

### 2. Store API Key as secret in Parameter store
```bash
aws ssm put-parameter --name "stock-api-key" --value "<API_KEY>" --type "SecureString"
```

### 3. Run Terraform commands
Initializes the directory
```bash
terraform init 
```
Format your configuration if needed 
```bash
terraform fmt 
```
Validate your configuration
```bash
terraform validate 
```
Apply the configuration and creates infrastructure
```bash
terraform apply
```
Terminates resources created by Terraform
```bash
terraform destroy  
```

### 4. Create subscription for SNS topic and subscribe to it
You can subscribe using email and/or SMS
![Screenshot 2025-01-12 163149](https://github.com/user-attachments/assets/fa33d1e1-fef5-423d-bc2f-f363de3c9ca6)
![Screenshot 2025-01-12 163157](https://github.com/user-attachments/assets/74ac425b-243e-4e27-8f8c-e8118dd726d9)
Then you will recieve a message and have to confirm 

![Screenshot 2025-01-12 163426](https://github.com/user-attachments/assets/d346edba-28f4-457e-92d5-ada91ad02d9e)


### 5. Test and Deploy Code 
Deploy the code. After test the code . (If any error occur try changing the timeout for the function from 3s to 6s or more.)
![image](https://github.com/user-attachments/assets/3e0be380-a667-47f0-9929-d6dd01da63cd)

Here is what a succesful test looks like:


![image](https://github.com/user-attachments/assets/b5b219df-11a3-485c-9273-eb1d93543e28)




### (Optional) Configure EventBridge Schedule to receive Notifcations at a certain period of time
![Screenshot 2025-01-12 171738](https://github.com/user-attachments/assets/bdbbd72b-6d4c-432c-be2e-3361abd187c0)


## What was learned 
- Create an SNS topic for users to subscribe too
- Setting up SNS to send messaseges 
- Create AWS services using Terraform
- Retirving data from an api and changing it to a readable format
- Tesing before delpoying your code
- 
## Future Improvements
- Have a link users and click to subsribe 
- Have a way to enter what stocks they want to see outside of changing the code inside the fuction 
