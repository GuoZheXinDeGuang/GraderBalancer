import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict

# Set page configuration
st.set_page_config(page_title="Score Distribution System", layout="wide")

# Function to calculate variance of scores
def calculate_variance(scores: List[float]) -> float:
    return np.var(scores) if scores else 0

# New function to divide scores into subsets
def divide_into_subsets(scores: List[float], k: int) -> List[List[float]]:
    subsets = [[] for _ in range(k)]
    subset_sums = [0] * k
    
    for score in sorted(scores, reverse=True):
        min_sum_index = subset_sums.index(min(subset_sums))
        subsets[min_sum_index].append(score)
        subset_sums[min_sum_index] += score
    
    return subsets

# Function to distribute questions using the new greedy approach
def distribute_questions(df: pd.DataFrame, graders: List[str]) -> Dict[str, List[float]]:
    scores = df['Score'].tolist()
    subsets = divide_into_subsets(scores, len(graders))
    return {grader: subset for grader, subset in zip(graders, subsets)}

# Title
st.title("Question Score Distribution System")

# Input for total number of questions
total_questions = st.number_input("Enter the total number of questions to be graded", min_value=1, value=1, step=1)

# Create a dataframe to store question scores
df = pd.DataFrame(index=range(1, total_questions + 1), columns=["Score"])

# Input scores for each question
st.subheader("Enter scores for each question")
for i in range(1, total_questions + 1):
    df.loc[i, "Score"] = st.number_input(f"Score for Question {i}", min_value=0.0, value=0.0, step=0.1, key=f"q_{i}")

# Button to trigger distribution
if st.button("Distribute Questions to Graders"):
    # Distribute questions among 4 graders
    graders = ["Grader A", "Grader B", "Grader C", "Grader D"]
    
    # Distribute questions using the new greedy algorithm
    grader_scores = distribute_questions(df, graders)
    
    # Display results
    st.subheader("Question Distribution Results")
    for grader, scores in grader_scores.items():
        st.write(f"**{grader}**")
        grader_df = pd.DataFrame({"Score": scores})
        st.table(grader_df)
        st.write(f"Total score: {sum(scores):.2f}")
        st.write(f"Mean score: {np.mean(scores):.2f}")
        st.write(f"Median score: {np.median(scores):.2f}")
        st.write(f"Score range: {max(scores) - min(scores):.2f}")
        st.write(f"Standard deviation: {np.std(scores):.2f}")
        st.write(f"Variance: {calculate_variance(scores):.4f}")
    
    # Calculate and display overall statistics
    st.subheader("Overall Statistics")
    total_score = df["Score"].sum()
    avg_score = df["Score"].mean()
    overall_variance = calculate_variance(df["Score"].tolist())
    st.write(f"Total score: {total_score:.2f}")
    st.write(f"Average score: {avg_score:.2f}")
    st.write(f"Overall variance: {overall_variance:.4f}")
    
    # Display distribution chart
    st.subheader("Question Score Distribution")
    st.bar_chart(df["Score"])

# Add some instructions and information
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Enter the total number of questions to be graded
2. Input a score for each question
3. Click the "Distribute Questions to Graders" button
4. View the distribution results and statistics
""")

st.sidebar.header("About")
st.sidebar.write("""
This application helps you distribute question grading tasks evenly among four graders.
It uses a greedy algorithm to minimize the variance of individual scores assigned to each grader.
The app provides detailed statistics for each grader and an overall score distribution chart.
""")
