import streamlit as st
import openai
import pdfplumber
import docx
import os


openai.api_key = os.getenv("OPENAI_API_KEY")

# Function is defined to extract text from PDF files
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Text is extracted page by page
    return text

# Function is defined to extract text from DOCX files
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])  # Text is extracted from each paragraph

# Function is defined to generate AI-generated text based on the provided prompt
import openai

# Function is updated to match OpenAI API v1.0+
def generate_ai_text(prompt):
    client = openai.OpenAI()  # Create OpenAI client

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert resume and cover letter writer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip() # AI response is extracted and returned

# Streamlit application title is set
st.title("AI Resume & Cover Letter Generator")

# File uploader is provided for users to upload their resume
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

# Text area is provided for users to input the job description
job_description = st.text_area("Paste Job Description")

# Input field is provided for users to specify important keywords
keywords = st.text_input("Enter specific words to include in cover letter (comma-separated)")

# Button is provided to trigger the generation of the resume and cover letter
if st.button("Generate Resume & Cover Letter"):
    if uploaded_file is not None and job_description:
        # File extension is identified
        file_extension = uploaded_file.name.split(".")[-1]
        
        # Text extraction is performed based on file type
        if file_extension == "pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif file_extension == "docx":
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file format.")  # Error message is displayed for unsupported files
            st.stop()
        
        # AI-generated resume bullet points are generated based on job description
        resume_prompt = f"Given the job description below, optimize the resume content:\nJob Description:\n{job_description}\nResume:\n{resume_text}"
        optimized_resume = generate_ai_text(resume_prompt)
        
        # AI-generated cover letter is generated including specified keywords
        cover_letter_prompt = f"Generate a personalized cover letter for the job description below. \nEnsure to include these keywords: {keywords}\nJob Description:\n{job_description}"
        cover_letter = generate_ai_text(cover_letter_prompt)
        
        # Optimized resume content is displayed
        st.subheader("Optimized Resume Suggestions")
        st.text_area("", optimized_resume, height=300)
        
        # AI-generated cover letter is displayed
        st.subheader("Generated Cover Letter")
        st.text_area("", cover_letter, height=300)
    else:
        st.error("Please upload a resume and provide a job description.")  # Error message is displayed if required inputs are missing
