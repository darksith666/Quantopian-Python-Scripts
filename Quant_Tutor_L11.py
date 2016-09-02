""" Lesson 11 - Putting it altogether
Basic trading algorithm  -- using mean reversion strategy
Hypothesis:  if the 10 day simple moving average is higher than its 30 day
simple moving average the price of the security will drop..conversly if short
SMA is lower than the long SMA, the price will go up.. this is referred to
as mean reversion"""

def initialize(context):
    """
    initialize() is called once at the start of the program. Any one-time
    startup logic goes here
    """

    #select assets to trade MSFT, UNH, CTAS, JNS, containing - chosen arbitrarily
    context.security_list = [sid(5061), sid(7792), sid(1941), sid(1746)]

    #Rebalance every Monday (or first trading day if holiday) at mkt open
    schedule_function(rebalance,
                        date_rules.every_day(),
                        time_rules.market_open())
""" Allocation to each security and determine long or short .  10 day sma below
30 day sma, we take long position-if 10 day above 30 day, short it.  also the
greater the relative difference between 10 day and 30 day, we take bigger position
"""
def compute_weights(context, data):
    """
    Compute weights for each security we want to order_target_percent
    """
    #Get the 30 day price history for each security
    hist = data.history(context.security_list, 'price', 30, '1d')

    #Create 10 day and 30 day trailing windows
    prices_10 = hist[-10:]
    prices_30 = hist

    #10 day and 30 day simple moving average (SMA)
    sma_10 = prices_10.mean()
    sma_30 = prices_30.mean()

    #Weights are based on the relative difference between the short and long SMAs
    raw_weights = (sma_30 - sma_10) / sma_30

    #Normalize our Weights
    normalized_weights = raw_weights / raw_weights.abs().sum()

    #Determine and log our long and shorts
    short_secs = normalized_weights.index[normalized_weights < 0]
    long_secs = normalized_weights.index[normalized_weights > 0]

    log.info("This week's longs: " + ", ".join([long_.symbol for long_ in long_secs]))
    log.info("This week's shorts:" + ", ".join([short_.symbol for short_ in short_secs]))

    #return normalized_weights
    return normalized_weights

def rebalance(context, data):
    """
    This function is called according to our schedule_function settings and calls
    order_target_percent() on every security in weights
    """

    #Calculate our target weights
    weights = compute_weights(context, data)

    #place orders for each of our securities
    for security in context.security_list:
        if data.can_trade(security):
            order_target_percent(security, weights[security])

def record_vars(context, data):
    """
    This function is called at the end of each day and plots our leverage
    as well as the number of long and short positions we are holding
    """

    #check how many long and short positions we have
    longs = shorts = 0
    for position in context.portfolio.positions.itervalues():
        if position.amount > 0:
            longs += 1
        elif position.amount < 0:
            shorts += 1
    #record our variables
    record(leverage = context.account.leverage, long_count = longs, short_count = shorts)
