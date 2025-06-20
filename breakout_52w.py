import pandas as pd
from strategy_base import Strategy

class Breakout52Week(Strategy):
    def generate_signals(self):
        high_52w = self.data['Close'].rolling(window=252).max()
        self.signals['signal'] = 0
        condition = self.data['Close'] > high_52w.shift(1)
        self.signals.loc[condition, 'signal'] = 1

        print(f"\n📊 52-Week Breakout: Total Signals: {condition.sum()}")
        return self.signals
