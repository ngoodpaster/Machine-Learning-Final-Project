# COEN 129 - Machine Learning Final Project
Here is the final version of our Machine Learning project for our COEN 129 class (Current Topics in Computer Engineering).  


Project Guidelines:

- Pick a real-world problem, describe your dataset, define your machine learning problem, apply a machine learning technique, and present the results. You are highly encouraged to use a large-scale dataset, i.e., at least 100K data instances.
- Projects can be done individually, or in teams of two students. For a group, group members are responsible for dividing up the work equally and making sure that each member contributes.
- If you are having trouble writing a proposal or executing the project, please feel free to consult withthe instructor.


Project Description:

- For our project, we decided to monitor selected stock options and use machine learning to predict the next day’s price. We then classify the stock with a buy, sell, or hold option based on the prediction.


Approach:
- Take given features:
  - Adjusted close
  - Adjusted volume
- Calculate new features:
  - Percent change from high/low
  - Volatility
  - Future price (output)
- Use a Decision Tree Regression model to predict the future price
  - Train on 49 days, test on one (current) day
  - Repeated this process for 20 days (for each stock)
- Categorize the price into BUY, SELL or HOLD categories
  - BUY when percent change > 5%
  - SELL when percent change is < -5%
  - HOLD otherwise 


File Description:

- In dataSet.py, we get all the data from the quandl dataset that we want, and store it in a text file, foo.txt.
- In features.py, we use the data in foo.txt to predict the future stock prices.


Data set info

- Using Quandl's free data set WIKI Prices - https://www.quandl.com/product/WIKIP/WIKI/PRICES-Quandl-End-Of-Day-Stocks-Info
- Quandl Documentation - https://docs.quandl.com/docs/tables-3#section-filter-rows
