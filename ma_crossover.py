import pandas as pd

class MovingAverageCrossover:
    def __init__(self, data: pd.DataFrame, short_window=50, long_window=200):
        self.data = data.copy()
        self.short_window = short_window
        self.long_window = long_window
        self.signals = pd.DataFrame(index=data.index)
        self.signals["signal"] = 0

    def generate_signals(self):
        short_sma = self.data["Close"].rolling(window=self.short_window).mean()
        long_sma = self.data["Close"].rolling(window=self.long_window).mean()
        condition = (short_sma > long_sma) & (short_sma.shift(1) <= long_sma.shift(1))
        self.signals.loc[condition, "signal"] = 1

        print(f"📊 MA Crossover Signals: {self.signals['signal'].sum()} total")
        return self.signals
