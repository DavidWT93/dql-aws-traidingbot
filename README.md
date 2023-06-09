# dql-aws-traidingbot

The project titled "dql-aws-tradingbot" demonstrates the implementation of a trading bot using AWS. The bot is designed to make predictions
on whether to buy or sell stocks. The project includes the training and construction of the underlying model, 
which can be found at: https://github.com/DavidWT93/dql-trading-bot-training/tree/master/sagemaker-train-test.

For a live demonstration of the model's predictions and a detailed explanation of the implementation, please visit my website: www.davidtillery.xyz.

## lambda function

The trading bot implementation utilizing AWS involves a Lambda function, which is responsible for extracting, transforming, and loading data into a
MySQL RDS database. The data is extracted from the ALPACA API, transformed by calculating technical indicators, and then loaded into the database.

## EC2 Insctance

An EC2 instance is utilized to run a Python script responsible for executing buy or sell orders based on the predictions made by the deep q learning algorithm. 
If the bot predicts that a particular stock will rise, it triggers a buy order, and if it predicts a decline, it initiates a sell order.

To ensure that the trading bot remains up-to-date, the script includes a feature that checks for a new model uploaded to an S3 bucket every day at midnight.
This ensures that the latest model is used for making predictions, as the model undergoes continuous training with new data.

The model retraining process is facilitated by a cronjob that runs a notebook at midnight each day, incorporating data from the previous 24 hours. 
More detailed information on training and retraining can be found at the link above.
