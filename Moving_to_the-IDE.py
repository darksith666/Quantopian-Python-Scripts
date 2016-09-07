#Lesson 12 - Moving to the IDE
from quantopian.pipeline import Pipeline
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.factors import SimpleMovingAverage, AverageDollarVolume
from quantopian.pipeline.filters.morningstar import IsPrimaryShare

def initialize(context):
    # Schedule our rebalance function to run at the start of each week.
    schedule_function(my_rebalance, date_rules.week_start(), time_rules.market_open(hours=1))

    # Record variables at the end of each day.
    schedule_function(my_record_vars, date_rules.every_day(), time_rules.market_close())

    # Create our pipeline and attach it to our algorithm.
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe, 'my_pipeline')

def make_pipeline():
    """
    Create our pipeline.
    """

    # Filter for primary share equities. IsPrimaryShare is a built-in filter.
    primary_share = IsPrimaryShare()

    # Equities listed as common stock (as opposed to, say, preferred stock).
    # 'ST00000001' indicates common stock.
    common_stock = morningstar.share_class_reference.security_type.latest.eq('ST00000001')

    # Non-depositary receipts. Recall that the ~ operator inverts filters,
    # turning Trues into Falses and vice versa
    not_depositary = ~morningstar.share_class_reference.is_depositary_receipt.latest

    # Equities not trading over-the-counter.
    not_otc = ~morningstar.share_class_reference.exchange_id.latest.startswith('OTC')

    # Not when-issued equities.
    not_wi = ~morningstar.share_class_reference.symbol.latest.endswith('.WI')

    # Equities without LP in their name, .matches does a match using a regular
    # expression
    not_lp_name = ~morningstar.company_reference.standard_name.latest.matches('.* L[. ]?P.?$')

    # Equities with a null value in the limited_partnership Morningstar
    # fundamental field.
    not_lp_balance_sheet = morningstar.balance_sheet.limited_partnership.latest.isnull()

    # Equities whose most recent Morningstar market cap is not null have
    # fundamental data and therefore are not ETFs.
    have_market_cap = morningstar.valuation.market_cap.latest.notnull()

    # Filter for stocks that pass all of our previous filters.
    tradeable_stocks = (
        primary_share
        & common_stock
        & not_depositary
        & not_otc
        & not_wi
        & not_lp_name
        & not_lp_balance_sheet
        & have_market_cap
    )

    # High dollar volume filter.
    base_universe = AverageDollarVolume(window_length=20, mask=tradeable_stocks).percentile_between(70, 100)

    # 10-day close price average.
    mean_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=base_universe)

    # 30-day close price average.
    mean_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=base_universe)

    percent_difference = (mean_10 - mean_30) / mean_30

    # Filter to select securities to short.
    shorts = percent_difference.top(25)

    # Filter to select securities to long.
    longs = percent_difference.bottom(25)

    # Filter for all securities that we want to trade.
    securities_to_trade = (shorts | longs)

    return Pipeline(
        columns={
            'longs': longs,
            'shorts': shorts
        },
        screen=(securities_to_trade),
    )

def my_compute_weights(context):
    """
    Compute ordering weights.
    """
    # Compute even target weights for our long positions and short positions.
    long_weight = 0.5 / len(context.longs)
    short_weight = -0.5 / len(context.shorts)

    return long_weight, short_weight

def before_trading_start(context, data):
    # Gets our pipeline output every day.
    context.output = pipeline_output('my_pipeline')

    # Go long in securities for which the 'longs' value is True.
    context.longs = context.output[context.output['longs']].index.tolist()

    # Go short in securities for which the 'shorts' value is True.
    context.shorts = context.output[context.output['shorts']].index.tolist()

    context.long_weight, context.short_weight = my_compute_weights(context)

def my_rebalance(context, data):
    """
    Rebalance weekly.
    """
    for security in context.portfolio.positions:
        if security not in context.longs and security not in context.shorts and data.can_trade(security):
            order_target_percent(security, 0)

    for security in context.longs:
        if data.can_trade(security):
            order_target_percent(security, context.long_weight)

    for security in context.shorts:
        if data.can_trade(security):
            order_target_percent(security, context.short_weight)

def my_record_vars(context, data):
    """
    Record variables at the end of each day.
    """
    longs = shorts = 0
    for position in context.portfolio.positions.itervalues():
        if position.amount > 0:
            longs += 1
        elif position.amount < 0:
            shorts += 1

    # Record our variables.
    record(leverage=context.account.leverage, long_count=longs, short_count=shorts)
