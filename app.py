import streamlit as st

st.title("主升段雷達")

stock = st.text_input("輸入股票代號")

if stock:
    st.write(f"股票代號：{stock}")
    st.write("技術面：80分")
    st.write("籌碼面：75分")
