#!/usr/bin/env python
# coding: utf-8


# In[ ]:


import pdfplumber
import docx

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


# In[16]:


import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Load BERT-based model for similarity matching
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_keywords(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN"]]

def calculate_similarity(resume_text, job_desc):
    resume_embedding = bert_model.encode(resume_text, convert_to_tensor=True)
    job_embedding = bert_model.encode(job_desc, convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
    return round(similarity_score * 100, 2)


# In[13]:


from fastapi import FastAPI, UploadFile, File
import shutil

app = FastAPI()

@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile, job_description: str):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file format"}

    # NLP Analysis
    keywords = extract_keywords(resume_text)
    similarity = calculate_similarity(resume_text, job_description)

    return {
        "resume_keywords": keywords,
        "match_score": similarity,
        "suggestion": "Add missing skills from job description to improve your match."
    }






