import streamlit as st

st.set_page_config(
    page_title="羽毛球数据中心",
    page_icon="🏸",
    layout="wide" # 宽屏模式，适合看图表
)

st.title("🏸 智能羽毛球分析系统")

st.markdown("""
### 欢迎使用
这是你的个人羽毛球数据中心。请从左侧侧边栏选择功能：

* **🔮 胜率预测**: 比赛中实时输入比分，AI 帮你算胜率。
* **📝 数据录入**: 打完球后，记录比赛结果。
* **🏆 排行榜**: 查看谁是胜场王。
* **⚔️ 雷达对比**: 选取两名选手，全方位对比能力。

---
*系统状态：已连接本地数据库*
""")

# 显示一张欢迎图片（可选）
st.image("https://images.unsplash.com/photo-1626224583764-84786c713608?ixlib=rb-4.0.3", use_container_width=True)