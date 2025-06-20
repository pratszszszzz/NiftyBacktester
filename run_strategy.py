from breakout_52w import Breakout52Week
from ma_crossover import MovingAverageCrossover
from rsi_strategy import RSIStrategy
from volume_spike import VolumeSpikeStrategy
from macd_strategy import MACDStrategy
from backtester import backtest_fixed_holding, summarize_results
import yfinance as yf
import pandas as pd


def fetch_data(symbol='RELIANCE.NS', start='2020-06-01', end='2025-06-01'):
    df = yf.download(symbol, start=start, end=end, interval='1d', group_by='ticker')
    if isinstance(df.columns, pd.MultiIndex):
        df = df.droplevel(0, axis=1)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
    df.index.name = 'Date'
    return df


def combine_signals(*signals_list):
    combined = signals_list[0].copy()
    combined['signal'] = 0
    for signals in signals_list:
        combined['signal'] += signals['signal']
    combined['signal'] = combined['signal'].clip(lower=-1, upper=1)
    return combined


if __name__ == "__main__":
    print("\n[Step 1] Choose dataset to run the strategy on:")
    print("1. NIFTY 50")
    print("2. NIFTY Midcap 100")
    print("3. NIFTY Smallcap 100")
    print("4. All NSE Listed Stocks")
    print("5. Individual Stock")
    print("6. From Custom CSV File")

    dataset_choice = input("Enter choice (1-6): ").strip()

    if dataset_choice == "1":
        df = pd.read_csv("nifty50.csv", usecols=['Symbol'])
        symbols = df['Symbol'].dropna().unique().tolist()
        batch_mode = True
    elif dataset_choice == "2":
        df = pd.read_csv("midcap100.csv", usecols=['Symbol'])
        symbols = df['Symbol'].dropna().unique().tolist()
        batch_mode = True
    elif dataset_choice == "3":
        df = pd.read_csv("smallcap100.csv", usecols=['Symbol'])
        symbols = df['Symbol'].dropna().unique().tolist()
        batch_mode = True
    elif dataset_choice == "4":
        df = pd.read_csv("all_nse_equity_symbols.csv", usecols=['Symbol'])
        symbols = df['Symbol'].dropna().unique().tolist()
        batch_mode = True
    elif dataset_choice == "5":
        symbol = input("Enter stock symbol (e.g., RELIANCE.NS): ").upper()
        symbols = [symbol]
        batch_mode = False
    elif dataset_choice == "6":
        csv_path = input("Enter path to CSV file with symbols (column 'Symbol'): ").strip()
        try:
            df_csv = pd.read_csv(csv_path, usecols=['Symbol'])
            symbols = df_csv['Symbol'].dropna().unique().tolist()
            batch_mode = True
        except Exception as e:
            print(f"[Error] Failed to load symbols from CSV: {e}")
            exit()
    else:
        print("[Error] Invalid dataset choice.")
        exit()

    print("\n[Step 2] Select strategy:")
    print("1. 52-Week High Breakout")
    print("2. Moving Average Crossover")
    print("3. RSI Strategy")
    print("4. Volume Spike Strategy")
    print("5. MACD Strategy")
    print("6. Combine Multiple Strategies")

    strategy_choice = input("Enter strategy choice (1 to 6): ").strip()
    selected_strategies = []

    if strategy_choice == "6":
        print("\n[Step 2.1] Choose strategies to combine (e.g., 1 3 5 for Breakout, RSI, MACD):")
        print("1. 52-Week High Breakout")
        print("2. Moving Average Crossover")
        print("3. RSI Strategy")
        print("4. Volume Spike Strategy")
        print("5. MACD Strategy")
        selected_strategies = input("Enter choices (space-separated): ").strip().split()

    positive_cagr = 0
    above_12_cagr = 0
    above_16_cagr = 0
    above_20_cagr = 0
    negative_cagr = 0
    top_12_names = []
    top_16_names = []
    top_20_names = []

    for symbol in symbols:
        try:
            print(f"\n[INFO] Fetching data for {symbol}...")
            data = fetch_data(symbol)

            if strategy_choice == "1":
                strategy = Breakout52Week(data)
                signals = strategy.generate_signals()
            elif strategy_choice == "2":
                strategy = MovingAverageCrossover(data, short_window=50, long_window=200)
                signals = strategy.generate_signals()
            elif strategy_choice == "3":
                strategy = RSIStrategy(data)
                signals = strategy.generate_signals()
            elif strategy_choice == "4":
                strategy = VolumeSpikeStrategy(data)
                signals = strategy.generate_signals()
            elif strategy_choice == "5":
                strategy = MACDStrategy(data)
                signals = strategy.generate_signals()
            elif strategy_choice == "6":
                signals_list = []
                for num in selected_strategies:
                    if num == "1":
                        s = Breakout52Week(data).generate_signals()
                    elif num == "2":
                        s = MovingAverageCrossover(data, 50, 200).generate_signals()
                    elif num == "3":
                        s = RSIStrategy(data).generate_signals()
                    elif num == "4":
                        s = VolumeSpikeStrategy(data).generate_signals()
                    elif num == "5":
                        s = MACDStrategy(data).generate_signals()
                    else:
                        continue
                    signals_list.append(s)
                signals = combine_signals(*signals_list)
            else:
                print("[Error] Invalid strategy choice.")
                continue

            print(f"[INFO] Running strategy on {symbol}")
            results = backtest_fixed_holding(data, signals, holding_days=5)
            cagr = summarize_results(results)

            if batch_mode:
                if cagr > 0:
                    positive_cagr += 1
                    if cagr > 12:
                        above_12_cagr += 1
                        top_12_names.append(symbol)
                    if cagr > 16:
                        above_16_cagr += 1
                        top_16_names.append(symbol)
                    if cagr > 20:
                        above_20_cagr += 1
                        top_20_names.append(symbol)
                else:
                    negative_cagr += 1
            else:
                from backtester import plot_trades
                plot_trades(data, results, symbol)

        except Exception as e:
            print(f"[WARNING] Error processing {symbol}: {e}")

    if batch_mode:
        print("\n[BATCH SUMMARY]")
        print(f"Positive CAGR Stocks: {positive_cagr}")
        print(f"Negative CAGR Stocks: {negative_cagr}")
        print(f"CAGR > 12%: {above_12_cagr} → {top_12_names}")
        print(f"CAGR > 16%: {above_16_cagr} → {top_16_names}")
        print(f"CAGR > 20%: {above_20_cagr} → {top_20_names}")
