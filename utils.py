import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sklearn
import numpy as np
import pandas as pd
from datetime import date
import datetime
import yfinance as yf
from ta.trend import MACD
from ta.momentum import StochasticOscillator

start_values = "2020-01-01"
today = date.today() + datetime.timedelta(days=1)
today_string = today.strftime("%Y-%m-%d")
current_year, current_month, current_day = today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")

# INCREASING_COLOR = '#30A03E'
# DECREASING_COLOR = '#E94C1A'
MOVING_AVERAGE_COLOR = '#2BA1EE'
BOLLINGER_BANDS_COLOR = '#ccc'

SP = {
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD',
    'Vet': 'VET-USD',
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Intel': 'INTC',
    'Tesla': 'TSLA',
    'Gold': 'GOLD',
    'Google': 'GOOG',
}


def get_all_market():
    """ Return dict of market dataframe """
    dico = {}
    for m in SP.keys():
        exec(f'dico["{m}"] = yf.download("{SP[m]}", start=start_values)')
    return dico


def get_one_market(market: str):
    """
    Return the dataframe of the given market
    :param market: the entier name of the market
    """
    res = {}
    try:
        exec(f'res["{market}"] = yf.download("{SP[market]}", start=start_values)')
        return res[market]
    except:
        raise NameError('Invalid market name')


def add_metrics(df: pd.DataFrame):
    """ add MA5 and MA20 Metrics in dataframe """
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['Date'] = df.index
    return df


def plot_market(df, INCREASING_COLOR, DECREASING_COLOR):
    # MACD
    macd = MACD(close=df['Close'],
                window_slow=26,
                window_fast=12,
                window_sign=9)

    # stochastic
    stoch = StochasticOscillator(high=df['High'],
                                 close=df['Close'],
                                 low=df['Low'],
                                 window=14,
                                 smooth_window=3)

    # add subplot properties when initializing fig variable
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        vertical_spacing=0.02,
                        row_heights=[0.5, 0.1, 0.2, 0.2])

    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='market data',
                                 increasing=dict(fillcolor=INCREASING_COLOR, line=dict(color=INCREASING_COLOR)),
                                 decreasing=dict(fillcolor=DECREASING_COLOR, line=dict(color=DECREASING_COLOR))))

    fig.add_trace(go.Scatter(x=df.index,
                             y=df['MA5'],
                             opacity=0.7,
                             line=dict(color='blue', width=2),
                             name='MA 5'))

    fig.add_trace(go.Scatter(x=df.index,
                             y=df['MA20'],
                             opacity=0.7,
                             line=dict(color='orange', width=2),
                             name='MA 20'))

    # Plot volume trace on 2nd row
    colors = ['green' if row['Open'] - row['Close'] >= 0
              else 'red' for index, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df.index,
                         y=df['Volume'],
                         marker_color=colors
                         ), row=2, col=1)

    # Plot MACD trace on 3rd row
    colorsM = ['green' if val >= 0
               else 'red' for val in macd.macd_diff()]
    fig.add_trace(go.Bar(x=df.index,
                         y=macd.macd_diff(),
                         marker_color=colorsM
                         ), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=macd.macd(),
                             line=dict(color='#84848E', width=2)
                             ), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=macd.macd_signal(),
                             line=dict(color='blue', width=1)
                             ), row=3, col=1)

    # Plot stochastics trace on 4th row
    fig.add_trace(go.Scatter(x=df.index,
                             y=stoch.stoch(),
                             line=dict(color='#84848E', width=2)
                             ), row=4, col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=stoch.stoch_signal(),
                             line=dict(color='blue', width=1)
                             ), row=4, col=1)

    # update layout by changing the plot size, hiding legends & rangeslider, and removing gaps between dates
    fig.update_layout(height=800,
                      showlegend=False,
                      xaxis_rangeslider_visible=False)

    # Make the title dynamic to reflect whichever stock we are analyzing
    fig.update_layout(
        yaxis_title='Stock Price',
    )

    # update y-axis label
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)
    fig.update_yaxes(title_text="Stoch", row=4, col=1)

    return fig
