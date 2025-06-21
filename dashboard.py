from breakout_52w import Breakout52Week
from ma_crossover import MovingAverageCrossover
from rsi_strategy import RSIStrategy
from volume_spike import VolumeSpikeStrategy
from macd_strategy import MACDStrategy
from backtester import backtest_fixed_holding, summarize_results
import yfinance as yf
import pandas as pd
import streamlit as st

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

def main():
    st.title("📈 Strategy Backtester Dashboard")

    dataset_choice = st.selectbox("Choose dataset to run the strategy on:", (
        "NIFTY 50", "NIFTY Midcap 100", "NIFTY Smallcap 100", "All NSE Listed Stocks", "Individual Stock", "From Custom CSV File"
    ))

    if dataset_choice == "NIFTY 50":
        df = pd.read_csv("nifty50.csv", usecols=['Symbol'])
    elif dataset_choice == "NIFTY Midcap 100":
        df = pd.read_csv("midcap100.csv", usecols=['Symbol'])
    elif dataset_choice == "NIFTY Smallcap 100":
        df = pd.read_csv("smallcap100.csv", usecols=['Symbol'])
    elif dataset_choice == "All NSE Listed Stocks":
        df = pd.read_csv("all_nse_equity_symbols.csv", usecols=['Symbol'])
    elif dataset_choice == "Individual Stock":
        symbol = st.text_input("Enter stock symbol (e.g., RELIANCE.NS):").upper()
        df = pd.DataFrame({'Symbol': [symbol]})
    elif dataset_choice == "From Custom CSV File":
        uploaded_file = st.file_uploader("Upload CSV file with 'Symbol' column")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, usecols=['Symbol'])
        else:
            st.stop()

    symbols = df['Symbol'].dropna().unique().tolist()

    strategy_choice = st.selectbox("Select strategy:", (
        "52-Week High Breakout", "Moving Average Crossover", "RSI Strategy", "Volume Spike Strategy", "MACD Strategy", "Combine Multiple Strategies"
    ))

    if strategy_choice == "Combine Multiple Strategies":
        multi_choices = st.multiselect("Choose strategies to combine:", [
            "52-Week High Breakout", "Moving Average Crossover", "RSI Strategy", "Volume Spike Strategy", "MACD Strategy"
        ])

    if st.button("Run Backtest"):
        positive_cagr = above_12_cagr = above_16_cagr = above_20_cagr = negative_cagr = 0
        top_12_names = []
        top_16_names = []
        top_20_names = []

        for symbol in symbols:
            with st.spinner(f"📥 Fetching data for {symbol}..."):
                try:
                    data = fetch_data(symbol)
                    if strategy_choice == "52-Week High Breakout":
                        signals = Breakout52Week(data).generate_signals()
                    elif strategy_choice == "Moving Average Crossover":
                        signals = MovingAverageCrossover(data, 50, 200).generate_signals()
                    elif strategy_choice == "RSI Strategy":
                        signals = RSIStrategy(data).generate_signals()
                    elif strategy_choice == "Volume Spike Strategy":
                        signals = VolumeSpikeStrategy(data).generate_signals()
                    elif strategy_choice == "MACD Strategy":
                        signals = MACDStrategy(data).generate_signals()
                    elif strategy_choice == "Combine Multiple Strategies":
                        signals_list = []
                        for strat in multi_choices:
                            if strat == "52-Week High Breakout":
                                signals_list.append(Breakout52Week(data).generate_signals())
                            elif strat == "Moving Average Crossover":
                                signals_list.append(MovingAverageCrossover(data, 50, 200).generate_signals())
                            elif strat == "RSI Strategy":
                                signals_list.append(RSIStrategy(data).generate_signals())
                            elif strat == "Volume Spike Strategy":
                                signals_list.append(VolumeSpikeStrategy(data).generate_signals())
                            elif strat == "MACD Strategy":
                                signals_list.append(MACDStrategy(data).generate_signals())
                        signals = combine_signals(*signals_list)
                    else:
                        st.error("Invalid strategy choice.")
                        continue

                    results = backtest_fixed_holding(data, signals, holding_days=5)
                    cagr = summarize_results(results)

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
                        st.success(f"{symbol} → CAGR: {cagr:.2f}%")
                    else:
                        negative_cagr += 1
                        st.error(f"{symbol} → CAGR: {cagr:.2f}%")

                except Exception as e:
                    st.warning(f"⚠️ {symbol} failed: {e}")

        st.subheader("📊 Summary:")
        st.write(f"Positive CAGR: {positive_cagr}")
        st.write(f"Negative CAGR: {negative_cagr}")
        st.write(f"CAGR > 12%: {above_12_cagr} → {top_12_names}")
        st.write(f"CAGR > 16%: {above_16_cagr} → {top_16_names}")
        st.write(f"CAGR > 20%: {above_20_cagr} → {top_20_names}")

if __name__ == "__main__":
    main()
