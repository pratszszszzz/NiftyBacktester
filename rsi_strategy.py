import pandas as pd
from strategy_base import Strategy

class RSIStrategy(Strategy):
    def __init__(self, data: pd.DataFrame, period: int = 14):
        super().__init__(data)
        self.period = period

    def calculate_rsi(self, series: pd.Series):
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(self.period).mean()
        avg_loss = loss.rolling(self.period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self):
        rsi = self.calculate_rsi(self.data['Close'])
        self.signals['signal'] = 0

        # 🔴 Short when RSI crosses above 30 (was buy)
        short_condition = (rsi > 30) & (rsi.shift(1) <= 30)
        self.signals.loc[short_condition, 'signal'] = -1

        # 🟢 Cover (buy) when RSI crosses below 70 (was sell)
        cover_condition = (rsi < 70) & (rsi.shift(1) >= 70)
        self.signals.loc[cover_condition, 'signal'] = 1

        print(f"\n📊 Reversed RSI Strategy: {self.signals['signal'].value_counts().to_dict()}")
        return self.signals
