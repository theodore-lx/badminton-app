import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="数据录入", page_icon="📝")
st.title("📝 比赛数据管理")

# 确保文件存在
csv_file = 'match_data.csv'

# 创建两个选项卡：手动录入 vs 批量导入
tab1, tab2 = st.tabs(["👋 手动录入", "📂 批量导入文件"])

# ==========================================
# 功能 1：手动录入 (Tab 1)
# ==========================================
with tab1:
    with st.form("match_form"):
        st.subheader("录入单场比赛")
        col1, col2 = st.columns(2)
        winner = col1.text_input("🏅 赢家姓名")
        loser = col2.text_input("💔 输家姓名")
        
        col3, col4 = st.columns(2)
        w_score = col3.number_input("赢家得分", 21)
        l_score = col4.number_input("输家得分", 0)
        
        st.markdown("---")
        st.write("📊 **赢家六边形评分**")
        rating_atk = st.slider("进攻能力", 0, 100, 80)
        rating_def = st.slider("防守能力", 0, 100, 80)
        rating_sta = st.slider("体能状况", 0, 100, 80)
        rating_men = st.slider("心态控制", 0, 100, 80)
        
        submitted = st.form_submit_button("💾 保存数据")

        if submitted:
            if not winner or not loser:
                st.error("请输入选手名字！")
            else:
                new_data = {
                    '日期': [datetime.date.today()],
                    '赢家': [winner],
                    '输家': [loser],
                    '赢家得分': [w_score],
                    '输家得分': [l_score],
                    '进攻评分': [rating_atk],
                    '防守评分': [rating_def],
                    '体能评分': [rating_sta],
                    '心态评分': [rating_men]
                }
                df_new = pd.DataFrame(new_data)
                # 使用 utf-8-sig 追加模式
                df_new.to_csv(csv_file, mode='a', header=False, index=False, encoding='utf-8-sig')
                st.success(f"✅ 成功记录：{winner} 胜 {loser}！")

# ==========================================
# 功能 2：批量导入 (Tab 2)
# ==========================================
with tab2:
    st.subheader("从 Excel / CSV 导入历史数据")
    st.info("💡 请确保上传的表格里包含这两列：'赢家', '输家' (其他列可选)")
    
    uploaded_file = st.file_uploader("拖拽文件到这里", type=['xlsx', 'xls', 'csv'])
    
    if uploaded_file is not None:
        try:
            # 读取文件
            if uploaded_file.name.endswith('.csv'):
                # 尝试多种编码读取 CSV
                try:
                    df_upload = pd.read_csv(uploaded_file, encoding='utf-8')
                except:
                    df_upload = pd.read_csv(uploaded_file, encoding='gbk')
            else:
                df_upload = pd.read_excel(uploaded_file)
            
            st.write("👀 预览你上传的数据前5行：")
            st.dataframe(df_upload.head())
            
            # 检查关键列
            if '赢家' not in df_upload.columns or '输家' not in df_upload.columns:
                st.error("❌ 错误：表格里必须有 '赢家' 和 '输家' 这两列！请修改表头后重试。")
            else:
                if st.button("🚀 确认导入系统"):
                    # 补全缺失的列（防止报错）
                    required_cols = ['日期', '赢家得分', '输家得分', '进攻评分', '防守评分', '体能评分', '心态评分']
                    for col in required_cols:
                        if col not in df_upload.columns:
                            # 如果表格里没写日期，就填今天；没写分数，就填默认值
                            val = datetime.date.today() if col == '日期' else 80
                            if '得分' in col: val = 0
                            df_upload[col] = val
                            
                    # 调整列顺序以匹配数据库
                    final_df = df_upload[['日期', '赢家', '输家', '赢家得分', '输家得分', '进攻评分', '防守评分', '体能评分', '心态评分']]
                    
                    # 追加保存
                    final_df.to_csv(csv_file, mode='a', header=False, index=False, encoding='utf-8-sig')
                    st.balloons()
                    st.success(f"🎉 成功导入了 {len(final_df)} 条比赛记录！")
                    
        except Exception as e:
            st.error(f"文件读取失败: {e}")