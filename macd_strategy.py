import pandas as pd
from strategy_base import Strategy

class MACDStrategy(Strategy):
    def __init__(self, data: pd.DataFrame, short_window=12, long_window=26, signal_window=9):
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window

    def generate_signals(self):
        close = self.data['Close']
        ema_short = close.ewm(span=self.short_window, adjust=False).mean()
        ema_long = close.ewm(span=self.long_window, adjust=False).mean()

        macd = ema_short - ema_long
        signal = macd.ewm(span=self.signal_window, adjust=False).mean()

        self.signals['signal'] = 0
        self.signals.loc[(macd > signal) & (macd.shift(1) <= signal.shift(1)), 'signal'] = 1
        self.signals.loc[(macd < signal) & (macd.shift(1) >= signal.shift(1)), 'signal'] = -1

        print(f"\n📊 MACD Strategy: {self.signals['signal'].value_counts().to_dict()}")
        return self.signals
