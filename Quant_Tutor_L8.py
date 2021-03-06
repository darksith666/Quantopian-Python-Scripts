""" Lesson 8 - Managing Your Portfolio and Plotting variables
current positions are stored in context.portfolio.positions - similiar to
Python dictionary having assets as keys and Position objects as values
"""
#close out each position in portfolio  iterate over the keys
for security in context.portfolio.positions:
    order_target_percent(security, 0)

#record() function plots time series charts updated as frequently as daily in
#backtesting or as frequently as minutely in live trading. up to 5 series

def initialize(context):
    context.aapl = sid(24)
    context.spy = sid(8554)

def reblance(context, data):
    order_target_percent(context.aapl, 0.50)
    order_target_percent(context.spy, -0.50)

def record_vars(context, data):

    long_count = 0
    short_count = 0

    for position in context.portfolio.positions.itervalues():
        if position.amount > 0:
            long_count += 1
        if position.amount < 0:
            short_count += 1

    #Plot the counts
    record(num_long = long_count, num_short = short_count)

""" Lesson 9 - Slippage and commission
simulation estimates the impact of orders on the fill rate and execution
price.  buy orders drive price up and sell order down  price_impact of the trade
volume_limit determines the fraction of a security's trading volume that can be
used by your algo"""

set_slippage(slippage.VolumeSharesSlippage(volume_limit = 0.025, price_impact = 0.1))

set_commission (commission.PerShare(cost = 0.0075, min_trade_cost = 1))
