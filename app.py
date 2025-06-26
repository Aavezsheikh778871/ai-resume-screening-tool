import streamlit as st
import pandas as pd
import os
from pdf_reader import extract_text_from_pdf
from resume_matcher import match_resumes
from skill_gap_analysis import analyze_skill_gap
import plotly.express as px

st.set_page_config(page_title="AI Resume Screening Tool", layout="centered")

st.title("🤖 AI Resume Screening Tool")
st.markdown("Upload a **Job Description** and scan resumes from the `resumes/` folder.")

# Load job description
jd_file = st.file_uploader("📄 Upload Job Description (.txt file)", type=["txt"])
resume_folder = "resumes"

if jd_file is not None:
    job_description = jd_file.read().decode("utf-8")

    if st.button("🚀 Match Resumes"):
        if not os.path.exists(resume_folder):
            st.error(f"❌ Resume folder '{resume_folder}' not found!")
        else:
            resume_texts = []
            resume_names = []

            for filename in os.listdir(resume_folder):
                if filename.endswith(".pdf"):
                    text = extract_text_from_pdf(os.path.join(resume_folder, filename))
                    resume_texts.append(text)
                    resume_names.append(filename)

            results = match_resumes(job_description, resume_texts, resume_names)

            # Save full results
            df = pd.DataFrame(results, columns=["Resume Name", "Match Score", "Matched Keywords"])
            df.to_csv("results.csv", index=False)

            # Top 3
            sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
            top_3 = sorted_results[:3]
            pd.DataFrame(top_3, columns=["Resume Name", "Match Score", "Matched Keywords"]).to_csv("top_3_shortlisted.csv", index=False)

            st.success("✅ Matching complete! Results saved.")

            # 📊 Show results
            st.subheader("📊 Resume Matching Results")
            st.dataframe(df)

            # 📈 Visual Scoring Dashboard
            st.subheader("📈 Visual Scoring Dashboard")
            fig = px.bar(df.sort_values("Match Score", ascending=False), x="Resume Name", y="Match Score",
                         color="Match Score", text="Match Score", color_continuous_scale="Blues")
            fig.update_layout(height=400)
            st.plotly_chart(fig)

            # 🏆 Show Top 3
            st.subheader("🏆 Top 3 Shortlisted")
            for name, score, keywords in top_3:
                st.markdown(f"**{name}** — Score: `{score:.2f}`")
                st.caption(f"Matched Skills: {', '.join(keywords)}")

else:
    st.warning("👆 Upload a job description file to begin.")
