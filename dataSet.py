import pandas as pd 
import numpy as np 
import quandl
from datetime import date
quandl.ApiConfig.api_key = "zCnMsnBTZogmUryumZCf"



def getStockPrices():
	
	initDate = date(2015,11,25)
	endDate = date(2016,12,31)


	ticker_list = []
	all_stocks = quandl.get_table('WIKI/PRICES', qopts = {'columns': ['ticker', 'adj_open']}, date = {'gte': initDate.strftime('%Y-%m-%d'), 'lte': initDate.strftime('%Y-%m-%d')})
	for index, row in all_stocks.iterrows():	
		if row.adj_open <= 5:
			ticker_list.append(str(row.ticker))

	feature_data = quandl.get_table('WIKI/PRICES', ticker = ticker_list, qopts = { 'columns': ['ticker', 'adj_close', 'adj_volume', 'adj_high', 'adj_low', 'adj_open', 'date'] }, date = { 'gte': initDate.strftime('%Y-%m-%d'), 'lte': endDate.strftime('%Y-%m-%d') }, paginate=True)

	data_array = np.array([0,0,0,0,0])
	ticker_id = np.array([0])
	name = ''
	j = 0
	i = 0
	remove = set()
	print ("Set: {}".format(remove))
	ticker_count = 0
	max_ticker_count = 0
	max_tick_index = set()
	for index, row in feature_data.iterrows():	
		if row.ticker != name:
			ticker_count = i
			if ticker_count > max_ticker_count:
				for _ in range(len(max_tick_index)):
					remove.add(max_tick_index.pop())
				#remove.add(max_tick_index)
				max_ticker_count = ticker_count
				max_tick_index.add(j)
			elif ticker_count < max_ticker_count:
				remove.add(j)
			else:
				max_tick_index.add(j)

			name = row.ticker
			j += 1
			i = 0
		

		adj_volume = row.adj_volume
		#If the volume is zero, add the ticker id to the remove set
		if (adj_volume == 0):	
			remove.add(j)

		adj_close = row.adj_close
		adj_high = row.adj_high
		adj_low = row.adj_low
		adj_open = row.adj_open
		newRow = np.array([adj_close, adj_volume, adj_high, adj_low, adj_open])
		data_array = np.vstack((data_array, newRow))
		ticker_id = np.vstack((ticker_id, j))
		i +=1

	print (max_ticker_count)
	ticker_id = ticker_id.astype(np.float64)
	data_array = np.append(data_array, ticker_id, 1)


	#loop through the array.  If a row's ticker id is in the set, delete that row.
	i = 0
	z = 1
	y = 0
	print (len(remove))
	while i < len(data_array):
		if int(data_array[i,-1]) in remove:
			print ("index: {} - tick: {}".format(i,data_array[i,-1]))
			data_array = np.delete(data_array, (i), axis=0)
		else:
			i+=1
	# #print(data_array.shape[0])
	# print (z)
	np.savetxt("foo.txt", data_array)

	
if __name__ == "__main__":

	getStockPrices()
