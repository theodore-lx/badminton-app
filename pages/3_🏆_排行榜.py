import streamlit as st
import pandas as pd

st.set_page_config(page_title="排行榜", page_icon="🏆")
st.title("🏆 选手胜场排行榜")

try:
    df = pd.read_csv('match_data.csv')
    
    # 简单的统计逻辑
    win_counts = df['赢家'].value_counts().reset_index()
    win_counts.columns = ['选手姓名', '胜场数']
    
    # 增加排名列
    win_counts.index = win_counts.index + 1
    
    st.table(win_counts)
    
    # 展示最近比赛记录
    st.subheader("📜 最近比赛记录")
    st.dataframe(df.tail(10)) # 只显示最后10场
    
except FileNotFoundError:
    st.error("暂无数据，请先去录入页面添加数据！")