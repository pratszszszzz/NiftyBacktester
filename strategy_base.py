import pandas as pd

class Strategy:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.signals = pd.DataFrame(index=data.index)
        self.signals["signal"] = 0  # 1 = Buy, -1 = Sell, 0 = Hold/Do nothing

    def generate_signals(self):
        raise NotImplementedError("You must implement the generate_signals() method.")
