import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")

# ---------------- CONFIG ----------------
TICKERS = ["AAPL", "MSFT", "SPY"]
START = "2015-01-01"
END = "2025-01-01"
TRADING_DAYS = 252          # trading days per year (for annualization)
ROLLING_WINDOW = 30         # days for rolling volatility / clustering plots
# ----------------------------------------


def download_prices(tickers, start, end):
    """
    Download price data for given tickers and date range.

    Returns a DataFrame with:
        index  = Date
        columns = tickers (one column per ticker)
        values = adjusted close (if available) or close prices.
    """
    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False,   # keep all OHLC + Adj Close
        progress=True,
    )

    # If we have multiple tickers, yfinance returns a MultiIndex columns
    # like: ('Adj Close', 'AAPL'), ('Adj Close', 'MSFT'), ...
    if isinstance(raw.columns, pd.MultiIndex):
        if "Adj Close" in raw.columns.get_level_values(0):
            data = raw["Adj Close"]
        else:
            # fallback: just use 'Close'
            data = raw["Close"]
    else:
        # single ticker case
        if "Adj Close" in raw.columns:
            data = raw["Adj Close"].to_frame()
        else:
            data = raw["Close"].to_frame()

    return pd.DataFrame(data)


def compute_returns(prices: pd.DataFrame):
    """
    Compute arithmetic (percentage) and log returns from price data.

    prices: DataFrame of prices with columns = tickers, index = dates.
    Returns:
        daily: DataFrame of arithmetic daily returns.
        log:   DataFrame of log daily returns.
    """
    daily = prices.pct_change().dropna()
    log = np.log(prices / prices.shift(1)).dropna()
    return daily, log


def summarize_risk_return(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Compute annualized return, volatility, Sharpe, and Sortino ratios
    for each asset given daily arithmetic returns.
    """
    daily_vol = daily_returns.std()
    mean_daily = daily_returns.mean()

    annual_vol = daily_vol * np.sqrt(TRADING_DAYS)
    annual_ret = (1 + mean_daily) ** TRADING_DAYS - 1

    # Sharpe (rf ~ 0)
    sharpe = (mean_daily / daily_vol) * np.sqrt(TRADING_DAYS)

    # Sortino: downside volatility only (negative returns)
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


def plot_volatility_clustering(
    daily_returns: pd.DataFrame,
    rolling_vol: pd.DataFrame,
    ticker: str = "AAPL",
    window: int = ROLLING_WINDOW,
):
    """
    Show daily returns and rolling annualized volatility for a single ticker
    to visualize volatility clustering.
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(daily_returns.index, daily_returns[ticker])
    axes[0].set_title(f"{ticker} Daily Returns")
    axes[0].axhline(0, color="black", linewidth=0.5)

    axes[1].plot(rolling_vol.index, rolling_vol[ticker])
    axes[1].set_title(f"{ticker} {window}-Day Rolling Annualized Volatility")
    axes[1].set_ylabel("Annualized Volatility")

    plt.tight_layout()
    plt.show()


def plot_risk_return_summary(summary: pd.DataFrame):
    """
    Plot bar charts for annualized return and annualized volatility.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    summary["Ann Return"].plot(kind="bar", ax=axes[0], title="Annualized Return")
    axes[0].set_ylabel("Return")

    summary["Ann Vol"].plot(kind="bar", ax=axes[1], title="Annualized Volatility")
    axes[1].set_ylabel("Volatility")

    plt.tight_layout()
    plt.show()


def main():
    # ---------- DATA ----------
    prices = download_prices(TICKERS, START, END)
    print(f"Downloaded prices shape: {prices.shape}")  # (n_days, n_assets)

    daily_ret, log_ret = compute_returns(prices)
    print(f"Daily returns shape: {daily_ret.shape}")

    # ---------- RISK/RETURN SUMMARY ----------
    summary = summarize_risk_return(daily_ret)
    print("\nRisk/Return summary:")
    print(summary)

    plot_risk_return_summary(summary)

    # ---------- TIME-SERIES ANALYSIS ----------
    cum_ret = (1 + daily_ret).cumprod() - 1
    rolling_vol = daily_ret.rolling(ROLLING_WINDOW).std() * np.sqrt(TRADING_DAYS)

    prices.plot(figsize=(12, 5), title="Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

    daily_ret.hist(bins=50, figsize=(12, 5))
    plt.suptitle("Histogram of Daily Returns")
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

    # Volatility clustering for a single asset
    plot_volatility_clustering(
        daily_ret, rolling_vol, ticker="AAPL", window=ROLLING_WINDOW
    )

    # ---------- EXPORT FOR LATER PROJECTS ----------
    summary.to_csv(os.path.join(BASE_DIR, "risk_return_summary.csv"))
    daily_ret.to_csv(os.path.join(BASE_DIR, "daily_returns.csv"))

    # return for interactive use (e.g., from a notebook)
    return prices, daily_ret, summary


if __name__ == "__main__":
    main()
