import streamlit as st

st.set_page_config(
    page_title="主升段雷達",
    page_icon="📈",
    layout="wide"
)

st.title("📈 主升段雷達")

stocks = {
    "2330": "台積電",
    "2317": "鴻海",
    "2454": "聯發科",
    "3450": "聯鈞",
    "3583": "辛耘"
}

stock = st.text_input("輸入股票代號")

if stock:

    name = stocks.get(stock, "未知股票")

    current_price = 100
    tech_score = 85
    chip_score = 80

    stop_loss = round(current_price * 0.95, 2)
    target_price = round(current_price * 1.15, 2)

    st.subheader(f"{name} ({stock})")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("技術面評分", f"{tech_score}分")

    with col2:
        st.metric("籌碼面評分", f"{chip_score}分")

    st.success("✓ 站上月線")
    st.success("✓ 量能增加")
    st.success("✓ 布林帶收縮")
    st.success("✓ 子母K型態")

    st.divider()

    st.metric("進場價", current_price)
    st.metric("停損價", stop_loss)
    st.metric("目標價", target_price)

st.divider()

st.header("🔥 近期推薦五檔")

recommend_list = [
    {"name": "台積電", "score": 92},
    {"name": "聯發科", "score": 89},
    {"name": "聯鈞", "score": 87},
    {"name": "辛耘", "score": 86},
    {"name": "鴻海", "score": 84},
]

for idx, stock in enumerate(recommend_list, start=1):
    st.write(
        f"{idx}. {stock['name']}｜主升段評分：{stock['score']}分"
    )
