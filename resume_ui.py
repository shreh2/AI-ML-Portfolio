import streamlit as st
import requests
from io import BytesIO

# Title
st.title("Resume Analyzer")
st.write("Upload your resume and provide a job description to see how well it matches!")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

# Job description input
job_description = st.text_area("Enter Job Description")

# Analyze button
if st.button("Analyze Resume"):
    if uploaded_file and job_description:
        # Convert file to bytes for API request
        files = {"file": (uploaded_file.name, BytesIO(uploaded_file.getvalue()))}
        data = {"job_description": job_description}

        # Debugging prints
        print("Sending request to API:", data)
        print("Uploading file:", uploaded_file.name)

        try:
            # Send request to FastAPI
            response = requests.post("http://127.0.0.1:8000/analyze_resume/", files=files, data=data)

            # Debugging prints
            print("Response Status Code:", response.status_code)
            print("Response Content:", response.text)

            # Handle API response
            if response.status_code == 200:
                result = response.json()
                st.subheader("Results")
                st.write(f"**Match Score:** {result['match_score']}%")
                st.write(f"**Extracted Keywords:** {', '.join(result['resume_keywords'])}")
                st.write(f"**Suggestions:** {result['suggestion']}")
            else:
                st.error(f"Error analyzing resume. Please try again.\nAPI Response: {response.text}")
        except Exception as e:
            st.error(f"API request failed: {str(e)}")
            print("API Request Error:", e)
    else:
        st.warning("Please upload a resume and enter a job description.")
