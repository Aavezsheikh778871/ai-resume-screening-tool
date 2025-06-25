import os
from pdf_reader import extract_text_from_pdf
from resume_matcher import match_resumes
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# Streamlit page setup
st.set_page_config(page_title="AI Resume Screening Tool", layout="wide")
st.title("🤖 AI Resume Screening Tool")

# Load job description
with open('job_description.txt', 'r', encoding='utf-8') as f:
    job_description = f.read()

st.subheader("📄 Job Description")
st.info(job_description)

# Read resumes from folder
resumes_folder = 'resumes'
resume_texts = []
resume_names = []

for filename in os.listdir(resumes_folder):
    if filename.endswith('.pdf'):
        path = os.path.join(resumes_folder, filename)
        text = extract_text_from_pdf(path)
        resume_texts.append(text)
        resume_names.append(filename)

if resume_texts:
    # Match resumes
    results = match_resumes(job_description, resume_texts, resume_names)

    # Sort and show results
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    top_3 = sorted_results[:3]

    # Convert to DataFrame for display
    df = pd.DataFrame(results, columns=["Resume Name", "Match Score", "Matched Keywords"])
    df['Match Score'] = df['Match Score'].apply(lambda x: round(x * 100, 2))

    st.subheader("📊 Matching Results")
    st.dataframe(df)

    # Save CSV files
    df.to_csv("results.csv", index=False)
    df.head(3).to_csv("top_3_shortlisted.csv", index=False)

    st.success("✅ Results saved to results.csv")
    st.success("✅ Top 3 resumes saved to top_3_shortlisted.csv")

    # Visualizations
    names = df['Resume Name']
    scores = df['Match Score']
    all_keywords = [kw for kws in df['Matched Keywords'] for kw in kws]

    # Bar Chart
    st.subheader("📊 Match Score Bar Chart")
    fig1, ax1 = plt.subplots()
    sns.barplot(x=scores, y=names, palette='viridis', ax=ax1)
    ax1.set_xlabel("Match Score (%)")
    ax1.set_ylabel("Resume")
    ax1.set_title("Resume Matching Score")
    st.pyplot(fig1)

    # Pie Chart
    st.subheader("🥧 Keyword Frequency (Pie Chart)")
    keyword_counts = Counter(all_keywords)
    labels = list(keyword_counts.keys())
    sizes = list(keyword_counts.values())
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    st.pyplot(fig2)

    # Word Cloud
    st.subheader("☁️ Matched Keyword Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(all_keywords))
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.imshow(wordcloud, interpolation='bilinear')
    ax3.axis('off')
    st.pyplot(fig3)

else:
    st.warning("⚠️ No PDF resumes found in the 'resumes' folder. Please add resumes and reload.")
