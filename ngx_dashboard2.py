import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# Trigger autorefresh every 30 minutes (1800000 ms)
st_autorefresh(interval=1800000, key="data_refresh")

# NGX tickers — replace with actual tickers if needed
stocks = {
    "Beta Glass": "BETAGLAS.LG",   # Replace with actual NGX tickers if different
    "Honeywell Flour": "HONYFLOUR.LG",
    "The Initiates Plc": "INITIATES.LG",
    "Academy Press": "ACADEMY.LG",
    "ABCTRANS": "ABCTRANS.LG"
}

weights = {
    "Beta Glass": 0.25,
    "Honeywell Flour": 0.20,
    "The Initiates Plc": 0.15,
    "Academy Press": 0.15,
    "ABCTRANS": 0.15
}

st.title("📊 NGX 3-Month Portfolio Dashboard")
st.markdown("### Target: 40% return | Risk Level: Moderate")

# Fetch Data
data = {}
for name, ticker in stocks.items():
    try:
        stock_data = yf.download(ticker, period="5d", interval="1d")
        latest_price = stock_data["Close"].iloc[-1]
        previous_price = stock_data["Close"].iloc[0]
        change = (latest_price - previous_price) / previous_price * 100
        data[name] = {
            "Price": round(latest_price, 2),
            "Change (%)": round(change, 2),
            "Weight": weights[name],
            "Gain (%)": round(change * weights[name], 2)
        }
    except:
        data[name] = {
            "Price": "N/A",
            "Change (%)": "N/A",
            "Weight": weights[name],
            "Gain (%)": "N/A"
        }

# Convert to DataFrame
df = pd.DataFrame(data).T
st.dataframe(df)

# Total Portfolio Return
valid_gains = df["Gain (%)"][df["Gain (%)"] != "N/A"]
if not valid_gains.empty:
    total_return = valid_gains.sum()
    st.markdown(f"### 📈 Portfolio Return: **{total_return:.2f}%**")
    if total_return >= 40:
        st.success("✅ Target Met!")
    else:
        st.warning("⚠️ Target Not Yet Met")
else:
    st.error("❌ No valid price data retrieved.")
