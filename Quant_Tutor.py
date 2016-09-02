#Quantopian Introductory Lessons
""" Lesson 1 - What is a trading algorithm?
Trading algo in Python defines two special functions: initialize() and
handle_data().  initialize() is called when the program is started and handle_data()
is called once per minute."""

#example - algo allocates 100% of portfolio to AAPL

def initialize(context):
    #Reference to AAPL
    context.aapl = sid(24)

def handle_data(context, data):
    #position 100% of our portfolio to be long in AAPL
    order_target_percent(context.aapl, 1.00)

""" Lesson 2 - Core functions
An algo on Quantopian has 3 core functions: initialize(), handle_data(),
and before_trading_start().  initialize() must be implemented in every algo
while handle_data() and before_trading_start() are optional"""

"""context is an augmented Python dictionary used for maintaining state
during backtest or live trading. context should be used instead of global
variables.  properties can be accessed using dot notation(context.some_property)
"""
def initialize(context):
    context.message = 'hello'

def handle_data(context, data):
    print context.message

"""Lesson 3 - Referencing Securities
best algos select securities using pipeline. Manual referencing:
sid() returns a security given a unique security ID--robust way as security's
SID never changes.  symbol() returns a security given a ticker symbol..not
robust as tickers can change"""

def initialize(context):
    context.aapl = sid(24)

def handle_data(context, data):
    print context.aapl

""" Lesson 4 - Ordering securities
Several functions that can be used to order securities in the Quantopian API
order_target_percent() allows ordering a security to a target percent of portfolio
(sum of open positions plus cash balance) Requires two arguements: asset being
ordered and target percent of portfolio
"""

#order_target_percent(sid(24), 0.50)

#open a short position
#order_target_percent(sid(24), -0.50)

#example- take long position in AAPL for 60% of portfolio and short SPY 40%

def initialize(context):
    context.aapl = sid(24)
    context.spy = sid(8554)

def handle_data(context, data):
    #Note: data.can_trade() is explained in next Lesson
    if data.can_trade(context.aapl):
        order_target_percent(context.aapl, 0.60)
    if data.can_trade(context.spy):
        order_target_percent(context.spy, -0.40)
