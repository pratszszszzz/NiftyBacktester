import pandas as pd
from strategy_base import Strategy

class VolumeSpikeStrategy(Strategy):
    def __init__(self, data: pd.DataFrame, volume_window: int = 20, volume_threshold: float = 2.0):
        super().__init__(data)
        self.volume_window = volume_window
        self.volume_threshold = volume_threshold

    def generate_signals(self):
        avg_volume = self.data['Volume'].rolling(window=self.volume_window).mean()
        volume_spike = self.data['Volume'] > self.volume_threshold * avg_volume

        # Price confirmation: Close price > previous day's Close
        price_momentum = self.data['Close'] > self.data['Close'].shift(1)

        self.signals['signal'] = 0
        self.signals.loc[volume_spike & price_momentum, 'signal'] = 1
        self.signals.loc[~price_momentum & volume_spike, 'signal'] = -1

        print(f"\n📊 Volume Spike Strategy: {self.signals['signal'].value_counts().to_dict()}")
        return self.signals
