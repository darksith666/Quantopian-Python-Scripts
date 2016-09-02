""" Lesson 7 - Scheduling functions
handle_data runs every minute. to trade at a different frequency
schedule_function allows custom functions at regular intervals including
interday and intraday timing"""
#example  schedule function rebalance()

schedule_function(func = rebalance,
                    date_rules = date_rules.every_day(),
                    time_rules = time_rules.market_open(hours = 1))

#example custom function weekly_trades() on the last trading day of each week
#30 minutes before market close
schedule_function(weekly_trades, date_rules.week_end(), time_rules.market_close(minutes = 30))

#takes long in SPY beginning of week and closes out the position at 3:30pm last day

def initialize(context):
    context.spy = sid(8554)

    schedule_function(open_positions, date_rules.week_start(), time_rules.market_open())
    schedule_function(close_positions, date_rules.week_end(), time_rules.market_close(minutes = 30))

def open_positions(context, data):
    order_target_percent(context.spy, 0.10)

def close_positions(context, data):
    order_target_percent(context.spy, 0)
