import os
from datetime import datetime

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")

TRADING_DAYS = 252
ROLLING_WINDOW = 30

# Always write files into the folder where THIS script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------- USER INPUT ----------

def get_user_params():
    """
    Ask the user which tickers and date range they want to analyze.

    Returns:
        tickers (list[str])
        start   (str, 'YYYY-MM-DD')
        end     (str, 'YYYY-MM-DD')
    """
    default_tickers = ["AAPL", "MSFT", "SPY"]
    default_start = "2015-01-01"
    default_end = "2025-01-01"

    # --- Tickers ---
    raw_tickers = input(
        f"Enter tickers separated by spaces "
        f"(press ENTER for default {default_tickers}): "
    ).strip()

    if not raw_tickers:
        tickers = default_tickers
    else:
        tickers = [t.strip().upper() for t in raw_tickers.split() if t.strip()]

    # --- Start date ---
    raw_start = input(
        f"Enter START date (YYYY-MM-DD, default {default_start}): "
    ).strip()

    if not raw_start:
        start = default_start
    else:
        start = validate_date_or_default(raw_start, default_start, label="start")

    # --- End date ---
    raw_end = input(
        f"Enter END date   (YYYY-MM-DD, default {default_end}): "
    ).strip()

    if not raw_end:
        end = default_end
    else:
        end = validate_date_or_default(raw_end, default_end, label="end")

    # Ensure end >= start (swap if user reversed them)
    try:
        dt_start = datetime.strptime(start, "%Y-%m-%d")
        dt_end = datetime.strptime(end, "%Y-%m-%d")
        if dt_end < dt_start:
            print(
                f"[WARN] End date {end} is before start date {start}. "
                "Swapping them."
            )
            start, end = end, start
    except ValueError:
        # If somehow parsing fails here, just keep as-is (we already validated above)
        pass

    print(f"[INFO] Using tickers: {tickers}")
    print(f"[INFO] Date range: {start} -> {end}")
    return tickers, start, end


def validate_date_or_default(raw: str, default: str, label: str) -> str:
    """
    Validate a date string in YYYY-MM-DD format.
    If invalid, print a warning and return the default.
    """
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        print(
            f"[WARN] Invalid {label} date '{raw}'. "
            f"Using default {default} instead."
        )
        return default


# ---------- CORE LOGIC ----------

def download_prices(tickers, start, end):
    """Download price data for given tickers and date range."""
    print(f"[INFO] Downloading prices for {tickers} from {start} to {end}...")

    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False,
        progress=True,
    )

    # Handle MultiIndex vs single-index columns
    if isinstance(raw.columns, pd.MultiIndex):
        if "Adj Close" in raw.columns.get_level_values(0):
            data = raw["Adj Close"]
        else:
            data = raw["Close"]
    else:
        if "Adj Close" in raw.columns:
            data = raw["Adj Close"].to_frame()
        else:
            data = raw["Close"].to_frame()

    data = pd.DataFrame(data)

    # Drop tickers with all-NaN data (likely invalid symbols)
    before_cols = list(data.columns)
    data = data.dropna(axis=1, how="all")
    after_cols = list(data.columns)

    removed = [c for c in before_cols if c not in after_cols]
    if removed:
        print(f"[WARN] No data for tickers {removed} – they will be ignored.")

    if data.empty:
        raise ValueError("No valid tickers with data. Please try again.")

    print("[INFO] Finished downloading. Shape:", data.shape)
    return data


def compute_returns(prices: pd.DataFrame):
    """Compute arithmetic (percentage) and log returns from price data."""
    daily = prices.pct_change().dropna()
    log = np.log(prices / prices.shift(1)).dropna()
    return daily, log


def summarize_risk_return(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """Compute annualized return, volatility, Sharpe, and Sortino ratios."""
    daily_vol = daily_returns.std()
    mean_daily = daily_returns.mean()

    annual_vol = daily_vol * np.sqrt(TRADING_DAYS)
    annual_ret = (1 + mean_daily) ** TRADING_DAYS - 1

    sharpe = (mean_daily / daily_vol) * np.sqrt(TRADING_DAYS)

    downside = daily_returns.copy()
    downside[downside > 0] = 0
    downside_vol = downside.std()
    sortino = (mean_daily / downside_vol) * np.sqrt(TRADING_DAYS)

    summary = pd.DataFrame(
        {
            "Ann Return": annual_ret,
            "Ann Vol": annual_vol,
            "Sharpe": sharpe,
            "Sortino": sortino,
        }
    )
    summary.index.name = "Ticker"
    return summary


# ---------- PLOTTING HELPERS ----------

def plot_volatility_clustering(
    daily_returns: pd.DataFrame,
    rolling_vol: pd.DataFrame,
    ticker: str,
    window: int = ROLLING_WINDOW,
):
    """Show daily returns and rolling annualized volatility for a single ticker."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(daily_returns.index, daily_returns[ticker])
    axes[0].set_title(f"{ticker} Daily Returns")
    axes[0].set_ylabel("Daily Return")
    axes[0].axhline(0, color="black", linewidth=0.5)

    axes[1].plot(rolling_vol.index, rolling_vol[ticker])
    axes[1].set_title(f"{ticker} {window}-Day Rolling Annualized Volatility")
    axes[1].set_ylabel("Annualized Volatility")
    axes[1].set_xlabel("Date")

    plt.tight_layout()
    plt.show()


def plot_risk_return_summary(summary: pd.DataFrame):
    """Plot bar charts for annualized return and annualized volatility."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    summary["Ann Return"].plot(kind="bar", ax=axes[0], title="Annualized Return")
    axes[0].set_ylabel("Return")
    axes[0].set_xlabel("Ticker")

    summary["Ann Vol"].plot(kind="bar", ax=axes[1], title="Annualized Volatility")
    axes[1].set_ylabel("Volatility")
    axes[1].set_xlabel("Ticker")

    plt.tight_layout()
    plt.show()


# ---------- MAIN PIPELINE ----------

def main():
    # 0. Ask user for tickers + date range
    tickers, start, end = get_user_params()

    # 1. Download prices
    prices = download_prices(tickers, start, end)

    # 2. Compute returns
    daily_ret, log_ret = compute_returns(prices)

    # 3. Risk/return summary
    summary = summarize_risk_return(daily_ret)
    print("\nRisk/Return summary:")
    print(summary)

    plot_risk_return_summary(summary)

    # 4. Time-series plots
    cum_ret = (1 + daily_ret).cumprod() - 1
    rolling_vol = daily_ret.rolling(ROLLING_WINDOW).std() * np.sqrt(TRADING_DAYS)

    prices.plot(figsize=(12, 5), title="Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

    daily_ret.hist(bins=50, figsize=(12, 8))
    plt.suptitle("Histogram of Daily Returns")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.show()

    cum_ret.plot(figsize=(12, 5), title="Cumulative Returns")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.show()

    rolling_vol.plot(
        figsize=(12, 5),
        title=f"{ROLLING_WINDOW}-Day Rolling Annualized Volatility",
    )
    plt.xlabel("Date")
    plt.ylabel("Annualized Volatility")
    plt.show()

    # Volatility clustering for the first valid ticker
    first_ticker = daily_ret.columns[0]
    plot_volatility_clustering(
        daily_ret, rolling_vol, ticker=first_ticker, window=ROLLING_WINDOW
    )

    # 5. Export CSVs for later projects
    daily_path = os.path.join(BASE_DIR, "daily_returns.csv")
    summary_path = os.path.join(BASE_DIR, "risk_return_summary.csv")

    daily_ret.to_csv(daily_path)
    summary.to_csv(summary_path)

    print(f"[INFO] Written daily returns to: {daily_path}")
    print(f"[INFO] Written risk/return summary to: {summary_path}")

    return prices, daily_ret, summary


if __name__ == "__main__":
    main()
