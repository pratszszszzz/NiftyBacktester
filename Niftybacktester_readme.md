# 📊 NiftyBacktester

A complete backtesting system with both CLI and Streamlit dashboard support for Indian stock market strategies.

---

## 🚀 Features

- Backtest across:

  - NIFTY 50
  - NIFTY Midcap 100
  - NIFTY Smallcap 100
  - All NSE-listed stocks (via CSV)
  - Individual stocks
  - Uploaded custom symbol lists

- 📊 Strategies Supported:

  - 52-Week High Breakout
  - Moving Average Crossover (50/200)
  - Reversed RSI Strategy
  - Volume Spike Strategy
  - MACD Strategy
  - Combine any number of strategies

- 🔎 For each symbol, the backtest reports:

  - Total Return
  - Return on Capital
  - Win Rate
  - Average Return per Trade
  - Annualized Return (CAGR)
  - ✅ Positive/Negative CAGR counts
  - 📍 Stocks with CAGR > 12%, >16%, >20%

---

## 📂 Project Structure

```
backtestStrategy/
│
├── breakout_52w.py               # 52-week high breakout
├── ma_crossover.py               # Moving average crossover
├── rsi_strategy.py               # Reversed RSI strategy
├── volume_spike.py               # Volume spike strategy
├── macd_strategy.py              # MACD strategy
├── strategy_base.py              # Base class for all strategies
├── backtester.py                 # Backtesting + summary tools
├── fetch_data_module.py         # Custom data fetching utilities
├── run_strategy.py               # CLI script to run backtests
├── dashboard.py                  # 📈 Streamlit-based dashboard
│
├── data/
│   ├── nifty50.csv                   # NIFTY 50 symbols (Symbol column only)
│   ├── midcap100.csv
│   ├── smallcap100.csv
│   └── all_nse_equity_symbols.csv   # All NSE equities from NSE
│
├── requirements.txt
└── README.md                         # You're here 👋
```

---

## 🛠️ Setup Instructions

1. **Create Virtual Environment:**

```bash
python -m venv .venv
```

2. **Activate Environment:**

- Windows: `..venv\Scripts\activate`
- Mac/Linux: `source .venv/bin/activate`

3. **Install Libraries:**

```bash
pip install -r requirements.txt
```

4. **Run CLI Version:**

```bash
python run_strategy.py
```

5. **Run Dashboard Version:**

```bash
streamlit run dashboard.py
```

---

## 📄 Input Format for Custom CSV

Ensure your custom symbol file has this format:

```
Symbol
RELIANCE.NS
HDFCBANK.NS
TCS.NS
```

---

## 🧐 Strategy Extension Guide

1. Create a new strategy file (e.g., `bollinger_bands.py`)
2. Inherit from `Strategy` in `strategy_base.py`
3. Implement `generate_signals()` method
4. Register the strategy in CLI (`run_strategy.py`) and dashboard (`dashboard.py`)

---

## 🧪 Example Backtest Output

```
Symbol: INFY.NS
Total Trades: 42
Win Rate: 61.9%
Return on Capital: ₹47,320
CAGR: 13.87%
```

---

## 📌 Dependencies

```txt
streamlit
yfinance
pandas
matplotlib
```

---

## ✅ Future Enhancements

- Add quarterly profit growth filters
- Add trailing stop-loss and position sizing
- Export results to CSV/Excel
- Live trade simulation using broker APIs

---

Made with 💡 by **Prathmesh Aglawe**

