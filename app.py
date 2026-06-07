import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="主升段雷達", layout="wide")

st.title("📈 主升段雷達")

stock = st.text_input("輸入台股代號", "2330")

if stock:

    ticker = stock + ".TW"

    try:
        df = yf.download(
            ticker,
            period="6mo",
            progress=False,
            auto_adjust=True
        )

        if len(df) < 60:
            st.error("資料不足")
            st.stop()

        close = float(df["Close"].iloc[-1])

        ma20 = float(df["Close"].rolling(20).mean().iloc[-1])
        ma60 = float(df["Close"].rolling(60).mean().iloc[-1])

        avg_volume = df["Volume"].rolling(20).mean().iloc[-1]
        current_volume = df["Volume"].iloc[-1]

        score = 0

        if close > ma20:
            score += 25

        if close > ma60:
            score += 25

        if current_volume > avg_volume:
            score += 25

        if ma20 > ma60:
            score += 25

        stop_loss = round(ma20, 2)
        target_price = round(close * 1.15, 2)

        st.subheader(f"{stock}")

        c1, c2, c3 = st.columns(3)

        c1.metric("目前股價", round(close, 2))
        c2.metric("主升段評分", score)
        c3.metric("目標價", target_price)

        st.metric("停損價", stop_loss)

        st.write("---")

        if close > ma20:
            st.success("✓ 站上20MA")

        if close > ma60:
            st.success("✓ 站上60MA")

        if current_volume > avg_volume:
            st.success("✓ 量能高於20日均量")

        if ma20 > ma60:
            st.success("✓ 均線多頭排列")

        st.line_chart(df["Close"])

    except Exception as e:
        st.error(str(e))
