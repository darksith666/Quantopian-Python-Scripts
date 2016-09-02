"""Lesson 10 - Managing orders
Necessary to control cash and leverage - to avoid overordering
look at open orders using get_open_orders()
 """

 # check on open orders before opening new ones

def initialize(context):
     #relatively illiquid stock
     context.xtl = sid(40768)

def handle_data(context, data):
    #Get all open orders
    open_orders = get_open_orders()

    if context.xtl not in open_orders and data.can_trade(context.xtl):
        order_target_percent(context.xtl, 0.05)
