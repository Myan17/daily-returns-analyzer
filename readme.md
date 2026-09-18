> **Archived — this project now lives in [quant-toolkit](https://github.com/Myan17/quant-toolkit).**
> Its code and full commit history are preserved there under
> [`legacy/daily-returns-analyzer`](https://github.com/Myan17/quant-toolkit/tree/main/legacy/daily-returns-analyzer).
> The rebuilt library adds tests, a walk-forward backtest, and fixes to the
> Sortino calculation and to weight/ticker alignment.

# 📈 Daily Returns & Volatility Analyzer  
### *A fully interactive quantitative finance tool for analyzing asset returns, volatility, and risk-adjusted performance.*

---

## 🚀 Overview

The **Daily Returns & Volatility Analyzer** is an interactive quantitative finance project that allows users to analyze **any tradable asset** simply by typing its ticker symbol and selecting the date range.

This project transforms raw financial data into **meaningful insights** used heavily in quantitative trading, risk management, and portfolio analysis.

Using downloadable price data from Yahoo Finance, the tool:

- downloads **any stock/ETF/crypto** supported on Yahoo Finance  
- computes **Arithmetic + Log returns**  
- measures **risk** using annualized volatility  
- evaluates **risk-adjusted performance** using Sharpe & Sortino ratios  
- visualizes **price trends**, **cumulative returns**, **histograms**, and **volatility clustering**  
- exports clean datasets for use in **future quant projects**  

This project builds the **core intuition needed to become a quant** and is the first module of a multi-project quantitative finance roadmap.

---

## 🎯 What This Project Does

### **1. Fully Interactive Stock Selection**
Users can now input:

- **Any number of tickers** (e.g., AAPL TSLA NVDA QQQ BTC-USD)
- **Your own start date**
- **Your own end date**

This makes the project flexible for **research, strategy testing, and market analysis**.

---

### **2. Downloads Historical Price Data**
Using `yfinance`, the script downloads:

- **Adjusted Close** prices  
- Over the exact date range you specify  
- For **multiple tickers at once**  

---

### **3. Computes Returns**
The project converts raw prices into:

#### 🟠 **Arithmetic Returns**
\[
r_t = \frac{P_t - P_{t-1}}{P_{t-1}}
\]

#### 🔵 **Log Returns**
\[
\ell_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
\]

Log returns add nicely over time and are heavily used in quant research.

---

### **4. Risk & Performance Metrics**
The tool computes:

- **Annualized Return**
- **Annualized Volatility**
- **Sharpe Ratio**
- **Sortino Ratio**
- **Downside Volatility**

These metrics are standard in hedge funds and quant finance.

---

### **5. Clean Visualizations & Diagnostics**
The tool generates **six key financial graphs**:

#### **1️⃣ Annualized Return (Bar Chart)**  
Compares long-term performance of assets.

#### **2️⃣ Annualized Volatility (Bar Chart)**  
Shows how risky each asset is.

#### **3️⃣ Price History Chart**  
Visualizes price trends, drawdowns, and market regimes.

#### **4️⃣ Histogram of Daily Returns**  
Reveals distribution shape and tail risks.

#### **5️⃣ Cumulative Returns**  
Shows growth of a $1 investment over time.

#### **6️⃣ Volatility Clustering Plot**  
Demonstrates real market dynamics like volatility spikes.

---

## 🧠 Concepts You Learn (Quant Finance Essentials)

### ✔ Arithmetic vs Log Returns  
Learn why quants prefer log returns for modeling.

### ✔ Volatility as Risk  
Daily volatility → Annualized volatility  
\[
\sigma_{annual} = \sigma_{daily} \times \sqrt{252}
\]

### ✔ Sharpe & Sortino Ratios  
Risk-adjusted performance measures.

### ✔ Volatility Clustering  
Real financial markets exhibit:  
- high volatility periods  
- low volatility periods  
- persistent regime behavior  

---

## 🔥 Unique & Standout Features

### ⭐ **1. User-Interactive Ticker Input**
Analyze ANY asset on Yahoo Finance:


### ⭐ **2. User-Interactive Date Range**
Choose ANY start and end date for comparisons.

### ⭐ **3. Smart Error Handling**
The script fixes:

- reversed dates  
- invalid formats  
- invalid tickers  

### ⭐ **4. Multi-Ticker Support**
Mix stocks, ETFs, and crypto in one analysis.

### ⭐ **5. Professional Visualizations**
Plots are clean and well-labeled for academic or professional use.

---

## 📂 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.11+** | Main language |
| **yfinance** | Market data downloader |
| **Pandas** | Data manipulation |
| **NumPy** | Mathematical operations |
| **Matplotlib** | Graphing |
| **CSV Export** | Saving datasets |
| **Virtualenv** | Environment management |

---

## ▶️ How to Run This Project

### **1. Navigate to project folder**
```bash
cd daily-returns

### **2. Activate virtual environment**

```bash
source .venv/bin/activate
```

### **3. Run the script**

```bash
./.venv/bin/python daily_returns_vol.py
```

### **4. Provide inputs when prompted**

**Example:**

```
Enter tickers: TSLA NVDA AAPL
Enter START date (YYYY-MM-DD): 2017-01-01
Enter END date (YYYY-MM-DD): 2024-01-01
```

---

## 🔍 How to Analyze Each Graph

### **Annualized Return**
Higher bar = better long-term performance.

### **Annualized Volatility**
Shows risk (higher volatility = more uncertainty).

### **Price History**
Useful for spotting:
- long-term momentum  
- bull/bear markets  
- drawdowns  

### **Daily Return Histograms**
Shows:
- distribution shape  
- tail risks  
- skewness  
- volatility differences  

### **Cumulative Returns**
Shows how an initial investment evolves over time.

### **Volatility Clustering**
Key insight into:
- financial crises  
- regime shifts  
- uncertainty spikes  
