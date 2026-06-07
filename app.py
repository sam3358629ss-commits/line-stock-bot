import streamlit as st

FINMIND_TOKEN = st.secrets["FINMIND_TOKEN"]
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="主升段雷達", layout="wide")

# =========================
# 股票池（可自行增加）
# =========================
AI_POOL = [
    "2330", "2454", "2303", "3711",
    "2382", "3231", "2356", "6669",
    "5274", "3035", "3443", "6533",
    "3017", "3583", "3450"
]

# =========================
# 評分函數
# =========================
def calc_score(close, ma20, ma60, volume, vol20):
    score = 0

    if close > ma20:
        score += 25

    if close > ma60:
        score += 25

    if ma20 > ma60:
        score += 25

    if volume > vol20:
        score += 25

    return score


# =========================
# 主畫面
# =========================
st.title("📈 主升段雷達")

# =========================
# TOP 5 推薦
# =========================
st.header("🔥 今日主升段 TOP 5")

results = []

with st.spinner("掃描股票池中..."):

    for code in AI_POOL:

        ticker = code + ".TW"

        try:
            df = yf.download(
                ticker,
                period="6mo",
                progress=False,
                auto_adjust=True
            )

            if df.空的 or len(df) < 60:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            close = float(df["Close"].iloc[-1])

            ma20 = float(
                df["Close"].rolling(20).mean().iloc[-1]
            )

            ma60 = float(
                df["Close"].rolling(60).mean().iloc[-1]
            )

            volume = float(df["Volume"].iloc[-1])

            vol20 = float(
                df["Volume"].rolling(20).mean().iloc[-1]
            )

            score = calc_score(
                close,
                ma20,
                ma60,
                volume,
                vol20
            )

            stop_loss = round(ma20, 2)
            target1 = round(close * 1.15, 2)
            target2 = round(close * 1.30, 2)

            results.append({
                "code": code,
                "score": score,
                "price": round(close, 2),
                "stop": stop_loss,
                "target1": target1,
                "target2": target2
            })

        except:
            pass

results = sorted(
    results,
    key=lambda x: x["score"],
    reverse=True
)

top5 = results[:5]

for i, s in enumerate(top5, start=1):

    st.markdown(
        f"""
### {i}. {s['code']}
- 主升段評分：**{s['score']}**
- 現價：**{s['price']}**
- 停損價：**{s['stop']}**
- 第一目標價：**{s['target1']}**
- 第二目標價：**{s['target2']}**
"""
    )

st.divider()

# =========================
# 個股分析
# =========================
st.header("🔍 個股分析")

stock = st.text_input("輸入台股代號", "2330")

if stock:

    df = None

    # 先找上市，再找上櫃
    for suffix in [".TW", ".TWO"]:
        try:
            test_df = yf.download(
                stock + suffix,
                period="6mo",
                progress=False,
                auto_adjust=True
            )

            if not test_df.empty and len(test_df) >= 60:
                df = test_df
                break

        except:
            pass

    if df is None:
        st.error("找不到股票代號或資料不足")
        st.stop()

    try:

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        close = float(df["Close"].iloc[-1])

        ma20 = float(
            df["Close"].rolling(20).mean().iloc[-1]
        )

        ma60 = float(
            df["Close"].rolling(60).mean().iloc[-1]
        )

        avg_volume = float(
            df["Volume"].rolling(20).mean().iloc[-1]
        )

        current_volume = float(
            df["Volume"].iloc[-1]
        )

        score = calc_score(
            close,
            ma20,
            ma60,
            current_volume,
            avg_volume
        )

        stop_loss = round(ma20, 2)
        target1 = round(close * 1.15, 2)
        target2 = round(close * 1.30, 2)

        st.subheader(f"{stock}")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "目前股價",
            round(close, 2)
        )

        c2.metric(
            "主升段評分",
            score
        )

        c3.metric(
            "停損價",
            stop_loss
        )

        st.metric(
            "第一目標價",
            target1
        )

        st.metric(
            "第二目標價",
            target2
        )

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
        st.error(f"發生錯誤: {str(e)}")
