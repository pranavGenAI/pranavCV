import streamlit as st
import base64
from PyPDF2 import PdfReader
import streamlit.components.v1 as components
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
import time
from streamlit_lottie import st_lottie
import requests
from groq import Groq
from langchain.embeddings import HuggingFaceEmbeddings

st.set_page_config(page_title="Pranav Baviskar", layout="wide", page_icon="🧑🏻‍💼")

st.header(':blue[Pranav Kishor Baviskar | Management Consultant | AI Enthusiast]')
st.write("Hey there, I'm Pranav! I'm passionate about leveraging data and technology to drive meaningful insights and solutions in business. Check out my LinkedIn profile on https://www.linkedin.com/in/pranav-baviskar/")

groq_api_key = "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"

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    You are Buddy, an AI assistant dedicated to assisting Pranav Baviskar in his job search by providing recruiters with relevant information.
    You will structure your answer properly to let the recruiter know only the skillsets and project experience matching the user's question.
    Limit your answer to 800 characters.
    If you do not know the answer, politely admit it and provide contact details for Pranav Baviskar for more information.
    Do not mention the source of your information.
    Here is the context to know more about Pranav: {context}
    Human: {question}
    Answer:
    """
    
    client = Groq(api_key=groq_api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(client, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = HuggingFaceEmbeddings()
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write(response)

def main():
    col4, col5 = st.columns([0.3, 0.7])
    
    with col4:
        st.header("AI Buddy")

    user_question = st.text_input("Type your questions and hit Enter to learn more about me from my AI Buddy!", key="user_question")
    
    if user_question:
        if st.button("Ask Question"):
            user_input(user_question)

if __name__ == "__main__":
    main()
