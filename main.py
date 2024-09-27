import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="评分分配系统", layout="wide")

# Set Chinese font (assuming a Chinese font is available in the system)
st.markdown("""
    <style>
    body {
        font-family: "Microsoft YaHei", sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("问题评分分配系统")

# Input for total number of questions
total_questions = st.number_input("请输入需要评分的问题总数", min_value=1, value=1, step=1)

# Create a dataframe to store question scores
df = pd.DataFrame(index=range(1, total_questions + 1), columns=["分数"])

# Input scores for each question
st.subheader("请为每个问题输入分数")
for i in range(1, total_questions + 1):
    df.loc[i, "分数"] = st.number_input(f"问题 {i} 的分数", min_value=0.0, value=0.0, step=0.1, key=f"q_{i}")

# Button to trigger distribution
if st.button("分配问题给评分员"):
    # Distribute questions evenly among 4 graders
    graders = ["评分员A", "评分员B", "评分员C", "评分员D"]
    num_graders = len(graders)
    
    # Create a list of grader assignments
    grader_assignments = []
    for i in range(total_questions):
        grader_assignments.append(graders[i % num_graders])
    
    # Assign graders to questions
    df["评分员"] = grader_assignments
    
    # Display results
    st.subheader("问题分配结果")
    for grader in graders:
        st.write(f"**{grader}**")
        grader_questions = df[df["评分员"] == grader]
        st.table(grader_questions[["分数"]])
    
    # Calculate and display statistics
    st.subheader("统计信息")
    total_score = df["分数"].sum()
    avg_score = df["分数"].mean()
    st.write(f"总分: {total_score:.2f}")
    st.write(f"平均分: {avg_score:.2f}")
    
    # Display distribution chart
    st.subheader("问题分数分布")
    st.bar_chart(df["分数"])

# Add some instructions and information
st.sidebar.header("使用说明")
st.sidebar.write("""
1. 输入需要评分的问题总数
2. 为每个问题输入分数
3. 点击"分配问题给评分员"按钮
4. 查看分配结果和统计信息
""")

st.sidebar.header("关于")
st.sidebar.write("""
这个应用程序可以帮助您将问题评分任务均匀地分配给四名评分员。
它还提供了基本的统计信息和分数分布图表。
""")
