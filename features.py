import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, cross_validation, svm, tree
from sklearn.linear_model import LinearRegression
import math
import time
#np.set_printoptions(threshold=np.nan)

def categorize(percent_change):
	stock_category = None
	if percent_change >= 5:
		stock_category = 0
	elif percent_change <= -5:
		stock_category = 1
	else:
		stock_category = 2
	print "category: {}".format(stock_category)
	return stock_category


def getData(link):
	data = pd.io.parsers.read_csv(
		filepath_or_buffer=link,
		header=None,
		sep=' ')
	data.dropna(how='all', inplace=True)
	data.tail()
	return data

def calculateRMSE(yExpected , yActual , size):
	mse = 0
	for i in range(size):
		diff = yActual[i] - yExpected[i]
		mse += math.pow(diff,2)
	rmse = math.sqrt(mse/size)
	return rmse

def analysis(df):
	#print df
	X = np.array(df[:,:-2])
	y = np.array(df[:,-1])
	
# Re-calculate actual category to test against
	y_fut = y[-2]
	y_trade = y[-3]
	y_per = ((y_fut - y_trade)/y_trade)*100
	y_cat = categorize(y_per)

	X = preprocessing.scale(X)

	test_size = int(.2 * X.shape[0])

	X_train = X[:-(test_size),:]
	X_test = X[-(test_size):,:]

	X_train = X[:-1,:]
	X_test = X[-1,:]
	y_train = y[:-1]
	y_test = y[-1]

	#clf = svm.SVR(kernel = "poly",degree = 3)
	clf = tree.DecisionTreeRegressor(max_depth=3)
	clf.fit(X_train,y_train)
	predictions = clf.predict(X_test)

	count = 0


	percent_change = ((predictions[0] - y_train[-2])/y_train[-2])*100
	predicted_cat = categorize(percent_change)
	if predicted_cat != y_cat:
		print ("Wrong")
	else:
		count += 1
		print ("Right")

	return predictions[0],count

if __name__ == "__main__":

	BUY = 0
	SELL = 0
	HOLD = 0
	link = 'foo.txt'
	df = getData(link)
	#print (df)
	data_array = np.array(df)
	#array for new features
	features = np.zeros((data_array.shape[0],7))

	# the first ticker number is 3
	j = 3
	buy_count= hold_count= sell_count = 0
	# starts at 1, because we need to use data from previous date for each row, (therefore cant start at 0)
	i = 1
	# we need to loop for the number of data points we will be using which is the size of the data_array - 3 rows for each stock (first 1 and last 2)
	# this gives us a range from 0 to size - 193*3
	for k in range(0,(data_array.shape[0])-(193*3)):
		#Check if in a new ticker group (skip first element if so)
		if (data_array[i+2][5] != j):
			j = data_array[i+2][5]
			i += 3
		#print (i)
		#Calculate price percent difference - 1st column
		prev_price = data_array[i-1][0]
		curr_price = data_array[i][0]
		price_diff = curr_price - prev_price
		features[k][0] = curr_price#(price_diff)/(prev_price)
		
		#Calculate volume percent difference - 2nd column
		#prev_vol = data_array[i-1][1]
		#vol_diff = data_array[i][1] - prev_vol
		features[k][1] = data_array[i][1]# (vol_diff)/(prev_vol)

		
		#Calculate percent change from high - 3rd column
		prev_high = data_array[i][2]
		price_diff_high = curr_price - prev_high
		features[k][2] = (price_diff_high)/prev_high

		#Calculate percent change from low - 4th column
		prev_low = data_array[i][3]
		price_diff_low = curr_price - prev_low
		features[k][3] = (price_diff_low)/prev_low

		#Calculate volatility - 5th column
		vola_diff = prev_high - prev_low
		features[k][4] = (vola_diff)/curr_price

		#future price - 6th clumn
		features[k][6] = data_array[i+1][0]

		#Calculate the future percent change - 7th column
		future_price = data_array[i+1][0]
		trade_price = data_array[i+1][4]
		#print ("future: {} - trade: {}".format(future_price,trade_price))
		percent_change = ((future_price - trade_price)/trade_price)*100
		#features[i][6] = percent_change
		stock_category = categorize(percent_change)
		if stock_category == 0:
			BUY+=1
		elif stock_category == 1:
			SELL+=1
		else:
			HOLD+=1
	
		features[k][5] = stock_category
		i+=1
	
	print (features)

	#get rid of zeros
	features = np.delete(features, 0, axis=0)
	features = np.delete(features, -1, axis=0)
	features = np.delete(features, -1, axis=0)

	increment = 274
	Rcount_total = 0
	days = np.arange(20)
	accuracy = np.zeros(193)
	acc = 0
	predictions_array = np.array(np.zeros(20))
	for i in range(193):
		Rcount = 0
		testing = features[(i*increment):increment*(i+1)]
		stock_prediction = np.zeros(20)
		actual_output = testing[48:68,6]
		for j in range(20):
			 stock_prediction[j],count = analysis(testing[j:50+j])
			 Rcount += count
			 Rcount_total += count
		predictions_array = np.vstack((predictions_array,stock_prediction))
		accuracy[i] = (Rcount/float(20))*100
		plt.figure()
		plt.plot(days, stock_prediction, 'b', label='predicted')
		plt.plot(days, actual_output, 'r', label="actual")
		plt.legend(loc='upper left')
		plt.xticks(np.arange(0,21,1))
		plt.title("Stock {}".format(i))
		plt.xlabel("Day")
		plt.ylabel("Price ($)")
	print ("{}".format(accuracy))
	acc = (Rcount_total/float(193*20))*100
	print ("{}".format(acc))
	plt.show()



