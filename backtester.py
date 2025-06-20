import pandas as pd
from datetime import datetime

def backtest_fixed_holding(data, signals, holding_days=5, initial_capital=100000):
    trades = []
    capital = initial_capital
    equity = capital
    equity_curve = []

    signals = signals.loc[data.index]
    signals = signals[signals['signal'] != 0]
    last_exit_date = None

    for entry_idx in range(len(signals)):
        signal_date = signals.index[entry_idx]
        signal_type = signals.iloc[entry_idx]['signal']

        # Ensure no overlapping trades
        if last_exit_date and signal_date <= last_exit_date:
            continue

        if signal_date not in data.index:
            continue

        try:
            entry_price = data.loc[signal_date]['Close']
            exit_idx = data.index.get_loc(signal_date) + holding_days
            if exit_idx >= len(data):
                continue

            exit_date = data.index[exit_idx]
            exit_price = data.loc[exit_date]['Close']

            qty = capital // entry_price
            if qty == 0:
                continue

            capital_deployed = qty * entry_price

            if signal_type == 1:
                pnl = (exit_price - entry_price) * qty
            elif signal_type == -1:
                pnl = (entry_price - exit_price) * qty
            else:
                continue

            capital += pnl  # Compounding
            equity = capital
            equity_curve.append((exit_date, equity))
            last_exit_date = exit_date

            trades.append({
                "Signal": "BUY" if signal_type == 1 else "SELL",
                "Entry Date": signal_date,
                "Entry Price": entry_price,
                "Exit Date": exit_date,
                "Exit Price": exit_price,
                "PnL": pnl,
                "Return (%)": (pnl / capital_deployed) * 100,
                "Capital Deployed": capital_deployed,
                "Equity": equity
            })

        except Exception as e:
            print(f"⚠️ Error processing signal at {signal_date}: {e}")
            continue

    return pd.DataFrame(trades)

def summarize_results(results):
    df = pd.DataFrame(results)
    total_trades = len(df)
    wins = df[df['PnL'] > 0]
    win_rate = len(wins) / total_trades * 100 if total_trades > 0 else 0
    total_return = df['PnL'].sum()
    capital = 100000  # fixed capital
    return_on_capital = (total_return / capital) * 100 if capital > 0 else 0

    start_date = df['Entry Date'].min()
    end_date = df['Exit Date'].max()
    years = (end_date - start_date).days / 365.0 if start_date and end_date else 1
    cagr = ((1 + (total_return / capital)) ** (1 / years) - 1) * 100 if years > 0 else 0

    print("\n📊 Performance Summary:")
    print(f"Total Trades: {total_trades}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Total Return: ₹{total_return:.2f}")
    print(f"Return on Capital: {return_on_capital:.2f}%")
    print(f"Average Return per Trade: ₹{df['PnL'].mean():.2f}")
    print(f"Annualized Return (CAGR): {cagr:.2f}%")

    return cagr



    # Plot equity curve
    '''plt.figure(figsize=(10, 4))
    plt.plot(trades_df['Exit Date'], trades_df['Equity'], marker='o')
    plt.title("Equity Curve")
    plt.xlabel("Exit Date")
    plt.ylabel("Equity (₹)")
    plt.grid(True)
    plt.ticklabel_format(style='plain', axis='y')  # no offset/scientific notation
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt

def plot_trades(data, trades_df, symbol):
    if trades_df.empty:
        print("\n⚠️ No trades to plot.")
        return

    plt.figure(figsize=(14, 6))
    plt.plot(data['Close'], label='Close Price', color='blue', alpha=0.6)

    # Plot Buy entries
    buy_trades = trades_df[trades_df['Signal'] == 'BUY']
    plt.scatter(buy_trades['Entry Date'], data.loc[buy_trades['Entry Date']]['Close'],
                marker='^', color='green', label='Buy Signal', s=80)

    # Plot Short entries
    sell_trades = trades_df[trades_df['Signal'] == 'SELL']
    plt.scatter(sell_trades['Entry Date'], data.loc[sell_trades['Entry Date']]['Close'],
                marker='v', color='red', label='Short Signal', s=80)

    plt.title(f"📈 Trade Entries - {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()'''
