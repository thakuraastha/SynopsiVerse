import streamlit as st
pip install streamlit PyPDF2 openai



import PyPDF2
import io
import os
import openai
from dotenv import load_dotenv

# Load the API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf_reader.getNumPages()
    full_text = ""

    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        full_text += page.extractText()

    return full_text

def summarize_text(text):
    prompt = f"Please summarize the following text:\n{text}"
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def chat_with_pdf(text, question):
    prompt = f"{text}\n\nUser: {question}\nAI:"
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

st.title("PDF Summarizer and Chat")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing PDF content..."):
        summary = summarize_text(text)

    st.markdown("**Summary:**")
    st.write(summary)

    question = st.text_input("Ask a question about the PDF content:")
    if question:
        with st.spinner("Generating response..."):
            answer = chat_with_pdf(text, question)

        st.markdown("**Answer:**")
        st.write(answer)
