import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Score Distribution System", layout="wide")

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
    # Distribute questions evenly among 4 graders
    graders = ["Grader A", "Grader B", "Grader C", "Grader D"]
    num_graders = len(graders)
    
    # Sort questions by score in descending order
    df_sorted = df.sort_values("Score", ascending=False)
    
    # Distribute questions in a round-robin fashion
    grader_assignments = []
    total_scores = {grader: 0 for grader in graders}
    for i, (_, row) in enumerate(df_sorted.iterrows()):
        current_grader = graders[i % num_graders]
        grader_assignments.append(current_grader)
        total_scores[current_grader] += row["Score"]
    
    # Assign graders to questions
    df["Grader"] = grader_assignments
    
    # Display results
    st.subheader("Question Distribution Results")
    for grader in graders:
        st.write(f"**{grader}**")
        grader_questions = df[df["Grader"] == grader]
        st.table(grader_questions[["Score"]])
        st.write(f"Total score for {grader}: {total_scores[grader]:.2f}")
    
    # Calculate and display statistics
    st.subheader("Statistics")
    total_score = df["Score"].sum()
    avg_score = df["Score"].mean()
    st.write(f"Total score: {total_score:.2f}")
    st.write(f"Average score: {avg_score:.2f}")
    
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
It also provides basic statistics and a score distribution chart.
""")
