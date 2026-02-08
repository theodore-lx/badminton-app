import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.set_page_config(page_title="胜率预测", page_icon="🔮")

st.title("🔮 实时胜率预测")

# 加载模型
try:
    model = joblib.load('badminton_model.pkl')
    features = joblib.load('model_features.pkl')
except:
    st.error("请先运行根目录下的 init_system.py！")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    my_score = st.number_input("我方得分", 0, 30, 0)
with col2:
    op_score = st.number_input("对方得分", 0, 30, 0)

streak = st.slider("当前连胜/连败", -5, 5, 0)
smash = st.number_input("我方累计杀球", 0, 50, 5)

if st.button("开始预测"):
    # 简单模拟预测逻辑（因为模型是初始化的）
    diff = my_score - op_score
    total = my_score + op_score
    
    # 构建输入
    input_data = pd.DataFrame([[diff, total, streak, smash]], columns=features)
    prob = model.predict_proba(input_data)[0][1]
    
    # 修正逻辑（之前写的）
    full_trust = 15.0
    conf = min(1.0, total / full_trust)
    final_prob = 0.5 + (prob - 0.5) * conf
    
    st.metric("预测胜率", f"{final_prob*100:.1f}%")
    st.progress(int(final_prob*100))