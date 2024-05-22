import streamlit as st
import base64
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
#from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
import time

st.set_page_config(page_title="Pranav Baviskar ", layout="wide",page_icon='🧑🏻‍💼')
st.write(os.getcwd())
st.markdown("""
    <style>
        @keyframes gradientAnimation {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        .animated-gradient-text_ {
            font-family: "Graphik Semibold";
            font-size: 42px;
            background: linear-gradient(45deg, rgb(245, 58, 126) 30%, rgb(200, 1, 200) 55%, rgb(197, 45, 243) 20%);
            background-size: 300% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientAnimation 10s ease-in-out infinite;
        }
        @keyframes animate_ {
            0%, 18%, 20%, 50.1%,60%, 65.1%, 80%,90.1%,92% {
                color: #0e3742;
                text-shadow: none;
                }
            18.1%, 20.1%, 30%,50%,60.1%,65%,80.1%,90%, 92.1%,100% {
                color: #fff;
                text-shadow: 0 0 10px rgb(197, 45, 243),
                             0 0 20px rgb(197, 45, 243);
                }
            }
        
        .animated-gradient-text_ {
                    font-family: "Graphik Semibold";
                    font-size: 42px;
                    color: #FFF;
                    transition: color 0.5s, text-shadow 0.5s;
                }

        .animated-gradient-text_:hover {
                    animation: animate_ 5s linear infinite;
                }

        
    </style>
    <p class="animated-gradient-text_">
        Pranav Baviskar | Management Consultant @ Accenture Strategy
    </p>
""", unsafe_allow_html=True)


#st.image("https://media1.tenor.com/m/6o864GYN6wUAAAAC/interruption-sorry.gif", width=1000)
# st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjl2dGNiYThobHplMG81aGNqMjdsbWwwYWJmbTBncGp6dHFtZTFzMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/CGP9713UVzQ0BQPhSf/giphy.gif", width=50)


# This is the first API key input; no need to repeat it in the main function.
api_key = st.secrets['GEMINI_API_KEY']

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

def get_vector_store(text_chunks, api_key):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    You are Buddy, an AI assistant dedicated to assisting Pranav Baviskar in his job search by providing recruiters with relevant and concise information. 
    If you do not know the answer, politely admit it and let recruiters know how to contact Pranav Baviskar to get more information. 
    Don't put "Buddy" or a breakline in the front of your answer.
    Here is the context to know more about Pranav: {context}
    Human: {question}
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    print("Prompt ***** --->", prompt)
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question, api_key):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    #new_db = FAISS.load_local("faiss_index", embeddings)
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    # speed = 10
    # container = st.empty()
    # tokens = response["output_text"].split()
    # for index in range(len(tokens) + 1):
    #     curr_full_text = " ".join(tokens[:index])
    #     container.markdown(curr_full_text)
    #     time.sleep(1 / speed)
    
    #Sample Example
    print('response is here......',response["output_text"])
    st.write("BidBooster: ", response["output_text"])
    #st.write("BidBooster: ", response["output_text"])

def main():
    st.header("Chat with BidBooster")
    st.markdown("""
    <style>
    input {
      border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    user_question = st.text_input("Ask a Question from the RFP Files", key="user_question")

    if user_question and api_key:  # Ensure API key and user question are provided
        if user_question:
            if st.button("Ask Question"):
                user_input(user_question, api_key)

    with st.sidebar:   
        st.markdown("""
            <style>
                @keyframes animate {
                    0%, 18%, 20%, 50.1%,60%, 65.1%, 80%,90.1%,92% {
                        color: #0e3742;
                        text-shadow: none;
                    }
                    18.1%, 20.1%, 30%,50%,60.1%,65%,80.1%,90%, 92.1%,100% {
                        color: #fff;
                        text-shadow: 0 0 10px #03bcf4,
                                    0 0 20px #03bcf4,
                                    0 0 40px #03bcf4,
                                    0 0 80px #03bcf4,
                                    0 0 160px #03bcf4;
                    }
                }

                .animated-gradient-text {
                    font-family: "Graphik Semibold";
                    font-size: 26px;
                    color: #FFF;
                    transition: color 0.5s, text-shadow 0.5s;
                }

                .animated-gradient-text:hover {
                    animation: animate 5s linear infinite;
                }

            </style>
            <p class = animated-gradient-text> BidBooster 💬 </p>    

        """, unsafe_allow_html=True)
        pdf_docs = "/mount/src/pranavcv/pranav_baviskar_cv.pdf"
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks, api_key)
        st.success("Type your questions and hit Enter to know more about me from my AI agent, Buddy!")
        st.image("https://lh3.googleusercontent.com/drive-viewer/AKGpihYU8EA7b_VKFOW3KfjRqOnyWczVTZkTRzAMwB2IQN23hdCaSh_J3EWOhb0Sc0m3ZKAzLn46tQr1ZrlGfXrCxGKb0WCIWJd5wzg=s2560", width = 400)
        
      #  st.image("https://media.tenor.com/s1Y9XfdN08EAAAAi/bot.gif", width=200)


if __name__ == "__main__":
    # with open('https://github.com/pranavGenAI/bidbooster/blob/475ae18b3c1f5a05a45ff983e06b025943137576/wave.css') as f:
        # css = f.read()

    st.markdown('''<style>
        .stApp > header {
        background-color: transparent;
    }
    .stApp {
        background: linear-gradient(45deg, #0a1621 20%, #0E1117 45%, #0E1117 55%, #3a5683 90%);
        animation: my_animation 20s ease infinite;
        background-size: 200% 200%;
        background-attachment: fixed;
    }
    @keyframes my_animation {
        0% {background-position: 0% 0%;}
        50% {background-position: 100% 100%;}
        100% {background-position: 0% 0%;}
    }
    [data-testid=stSidebar] {
        background: linear-gradient(360deg, #1a2631 95%, #161d29 10%);
    }
    div.stButton > button:first-child {
        background:linear-gradient(45deg, #c9024b 45%, #ba0158 55%, #cd006d 70%);
        color: white;
        border: none;
    }
    div.stButton > button:hover {
        background:linear-gradient(45deg, #ce026f 45%, #970e79 55%, #6c028d 70%);
        background-color:#ce1126;
    }
    div.stButton > button:active {
        position:relative;
        top:3px;
    }    


    </style>''', unsafe_allow_html=True)
    main()
