"""Quantopian Pipeline Lesson Masking
When necessary to ignore certain assets when computing pipeline expressions

 """
from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import SimpleMovingAverage, AverageDollarVolume

def make_pipeline():
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length = 30)

    percent_difference = (mean_close_10 - mean_close_30) / mean_close_30

    dollar_volume = AverageDollarVolume(window_length=30)
    high_dollar_volume = dollar_volume.percentile_between(90, 100)

    latest_close = USEquityPricing.close.latest
    above_20 = latest_close > 20

    tradeable_filter = high_dollar_volume & above_20

    return Pipeline(
        columns= {
            'percent_difference' : percent_difference
        },
        screen = tradeable_filter)


result = run_pipeline(make_pipeline(), '2015-05-05', '2015-05-05')
print 'Number of securities that passed the filter: %d' % len(result)
result
