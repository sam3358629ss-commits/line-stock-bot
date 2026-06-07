import streamlit as st

st.title("📈 主升段雷達")

stock = st.text_input("輸入股票代號", placeholder="例如：2330")

if stock:
    st.subheader(f"股票代號：{stock}")

    st.metric("技術面", "80分")
    st.metric("籌碼面", "75分")

    st.success("✓ 站上月線")
    st.success("✓ 量能增加")
    st.success("✓ 布林帶收縮")
