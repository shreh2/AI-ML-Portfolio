import streamlit as st
import requests

st.title("📄 Resume Analyzer")
st.write("Upload your resume and provide a job description to see how well it matches!")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

# Job description input
job_description = st.text_area("Enter Job Description")

# Analyze button
if st.button("Analyze Resume"):
    if uploaded_file and job_description:
        # Send request to FastAPI backend
        files = {"file": uploaded_file.getvalue()}
        data = {"job_description": job_description}
        response = requests.post("http://127.0.0.1:8000/analyze_resume/", files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            st.subheader("Results")
            st.write(f"**Match Score:** {result['match_score']}%")
            st.write(f"**Extracted Keywords:** {', '.join(result['resume_keywords'])}")
            st.write(f"**Suggestions:** {result['suggestion']}")
        else:
            st.error("Error analyzing resume. Please try again.")
    else:
        st.warning("Please upload a resume and enter a job description.")
