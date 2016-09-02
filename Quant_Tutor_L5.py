""" Lesson 5 - The Data Object
data object - look up current or historical pricing and volume data for
any security. data is available in handle_data() and before_trading_start()
as well as any scheduled functions.
data.current() - return most recent value of given field(s) for a given asset(s)
Requires two arguements: the asset or list of assets and the field or list of
fields being queried. Possible fields include 'price', 'open', 'high', 'low',
'close', and 'volume'.
 """
 data.current(sid(24), 'price') #get most recent price
 data.current([sid(24), sid(8554)], 'price') # return panda series indexed by asset
 """get last known low and high prices returns pandas DataFrame(indexed by assets
 fields as columns)"""

 data.current([sid(24), sid(8554)], ['low', 'high'])

 data.can_trade(sid(24))

 """ Lesson 6 - The histoy Function
 data object has a function history() which gets trailing windows of historical
 pricing or volume data.  data.history() Requires 4 arguments:
 an asset or list of assets, a field or list of fields, an integer lookback window
 and a lookback frequency"""


#example: returns a pandas series containing price history of AAPL over last 10 days

hist = data.history(sid(24), 'price', 10, '1d')

#mean price over the last 10 days
mean_price = hist.mean()
#'1d' frequency the most recent value in data.history() will be current
#date which could be partial day
#10 complete days

data.history(sid(8554), 'volume', 11, '1d')[:1].mean()

#return type of data.history() depends on input types - eg returns pandas DF
#get last 5 minutes of volume data for each security in our list
hist = data.history([side(24), sid(8554), sid(5061)], 'volume', 5, '1m')
#calculate the mean volume for each security in our DataFrame
mean_volumes = hist.mean(axis = 0)

#if we pass list of fields, return pandas Panel indexed by field, having date
#as major axis and assets as minor axis

#low and high minut bar histor for each security
hist = data.history([sid(24), sid(8554), sid(5061)], 'low', 'high', 5, '1m')

#calculate the mean low and high over the last 5 minutes
means = hist.mean()
mean_lows = means.['low']
mean_highs = means['high']

def initialize(context):
    #AAPL, MSFT, SPY
    context.security_list = [sid(24), sid(8554), sid(5061)]

def handle_data(context, data):
    hist = data.history(context.security_list, 'volume', 10, '1m').mean()
    print hist.mean()
