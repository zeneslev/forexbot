from backtesting import Strategy
from backtesting.lib import crossover
from backtesting import Backtest
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import csv 


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()

class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20
    
    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
    
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

#Load up data
df = pd.read_csv("USD_JPY_M5.csv", parse_dates=["DateTime"]) #Set the time column to be datetime objects
df.set_index('DateTime', inplace=True) #Make dataframe indexable by datetime

bt = Backtest(df, SmaCross, cash=3_000, commission=0)

stats, heatmap = bt.optimize(n1=range(5, 30, 10),
                    n2=range(10, 200, 10),
                    maximize='Equity Final [$]',
                    constraint=lambda param: param.n1 < param.n2,
                    return_heatmap = True)

# bt = Backtest(GOOG, SmaCross, cash=3_000, commission=.002)
#stats = bt.run()
#print(stats)

hm = heatmap.unstack()
print(hm)
sns.heatmap(hm, cmap="cool")
#plt.show()
plt.savefig(fname="heatmap.png", format="png")
#bt.plot(plot_volume=False, plot_pl=False)

#hm = heatmap.groupby['n1','n2'].mean()
#print(hm)
#print(stats['_trades'])

#bt.plot()