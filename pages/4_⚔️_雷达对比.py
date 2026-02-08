import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="雷达对比", page_icon="⚔️")
st.title("⚔️ 选手能力雷达对比")

try:
    df = pd.read_csv('match_data.csv')
    
    # 获取所有出现过的选手名字
    all_players = list(set(df['赢家'].unique()))
    
    col1, col2 = st.columns(2)
    p1 = col1.selectbox("选择选手 A", all_players, index=0)
    # 尝试默认选另一个
    idx2 = 1 if len(all_players) > 1 else 0
    p2 = col2.selectbox("选择选手 B", all_players, index=idx2)
    
    # 计算平均分函数的逻辑
    def get_avg_stats(player_name):
        # 找出这个选手作为赢家时的记录 (简化逻辑：只统计赢球时的表现)
        # 如果要做得更细，录入时也要录入输家的评分
        stats = df[df['赢家'] == player_name][['进攻评分', '防守评分', '体能评分', '心态评分']]
        if stats.empty:
            return [50, 50, 50, 50] # 没数据就给平均分
        return stats.mean().tolist()

    if st.button("开始对比"):
        stats1 = get_avg_stats(p1)
        stats2 = get_avg_stats(p2)
        
        categories = ['进攻', '防守', '体能', '心态']
        
        fig = go.Figure()

        # 选手A
        fig.add_trace(go.Scatterpolar(
            r=stats1 + [stats1[0]], # 闭环
            theta=categories + [categories[0]],
            fill='toself',
            name=p1,
            line_color='blue'
        ))
        
        # 选手B
        fig.add_trace(go.Scatterpolar(
            r=stats2 + [stats2[0]], # 闭环
            theta=categories + [categories[0]],
            fill='toself',
            name=p2,
            line_color='red'
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("还没有比赛数据，无法对比！请先录入。")