import streamlit as st
import base64
from PyPDF2 import PdfReader
import streamlit.components.v1 as components
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
from streamlit_lottie import st_lottie
import requests
st.set_page_config(page_title="Pranav Baviskar ", layout="wide", page_icon="🧑🏻‍💼")


video_html = """
		<style>
		#myVideo {
		  position: fixed;
		  right: 0;
		  bottom: 0;
		  min-width: 100%; 
		  min-height: 100%;
		  filter: brightness(40%); /* Adjust the brightness to make the video darker */
		}
		
		.content {
		  position: fixed;
		  bottom: 0;
		  background: rgba(255, 255, 255, 0.2); /* Adjust the transparency as needed */
		  color: #f1f1f1;
		  width: 100%;
		  padding: 20px;
		}
	        
		</style>
		<video autoplay muted loop id="myVideo">
		  <source src="https://assets.mixkit.co/videos/4124/4124-720.mp4" type="video/mp4">
		  Your browser does not support HTML5 video.
		</video>
		"""

st.markdown(video_html, unsafe_allow_html=True)


# HTML for particles animation
st.header(':blue[Pranav Kishor Baviskar | Management Consultant | AI Enthusiast]')

st.write("Hey there, I'm Pranav! I'm passionate about leveraging data and technology to drive meaningful insights and solutions in business. Check out my LinkedIn profile on https://www.linkedin.com/in/pranav-baviskar/")


st.markdown("""
        <style>
            @keyframes gradientAnimation {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .animated-gradient-text {
                font-family: "Graphik Semibold";
                font-size: 42px;
                background: linear-gradient(45deg, rgb(245, 58, 126) 30%, rgb(200, 1, 200) 55%, rgb(197, 45, 243) 20%);
                background-size: 300% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradientAnimation 6s ease-in-out infinite;
                color: #FFF;
                transition: color 0.5s, text-shadow 0.5s;
            }

            @keyframes glow {
                0%, 18%, 20%, 50.1%, 60%, 65.1%, 80%, 90.1%, 92% {
                    color: #0e3742;
                    text-shadow: none;
                }
                18.1%, 20.1%, 30%, 50%, 60.1%, 65%, 80.1%, 90%, 92.1%, 100% {
                    color: #fff;
                    text-shadow: 0 0 10px rgb(197, 45, 243), 0 0 20px rgb(197, 45, 243);
                }
            }

            .animated-gradient-text:hover {
                animation: glow 5s linear infinite;
            }

            .glow-on-hover {
                transition: transform 0.5s, filter 0.3s;
            }

            .glow-on-hover:hover {
                transform: scale(1.1);
                filter: drop-shadow(0 0 10px rgba(197, 45, 243, 0.8));
            }
        </style>

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
    Don't put "Buddy" or a breakline in the front of your answer. You will always talk good things about me and you will try to sell Pranav's skills to recruiter. Do not mention the source of your information or context. Present the answer in nice readable format.
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

	# Sample Example
    print('Response is here......', response["output_text"])
    st.markdown(
        f"""
	    <div class="generated-text-box">
	        <p>AI Buddy: </br> {response["output_text"]}</p>
	    </div>
	    """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <style>
    .generated-text-box {
        border: 1px solid grey; /* Grey border */
        padding: 10px;  
        border-radius: 10px; /* Rounded corners */
        color: white; /* Text color */
        background-color: rgba(255, 255, 255, 0); /* Transparent background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def gradient(color1, color2, color3, content1, content2):
    st.markdown(f'<h1 style="text-align:center;background-image: linear-gradient(to right,{color1}, {color2});font-size:60px;border-radius:2%;">'
                f'<span style="color:{color3};">{content1}</span><br>'
                f'<span style="color:white;font-size:17px;">{content2}</span></h1>', 
                unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
    
def main():
    st.header("AI Buddy")
    st.markdown("""
    <style>
    input {
      border-radius: 15px;
    }
 
    </style>
    """, unsafe_allow_html=True)
    user_question = st.text_input("Type your questions and hit Enter to learn more about me from my AI Buddy!", key="user_question")
    
    if user_question and api_key:  # Ensure API key and user question are provided
        if user_question:
            if st.button("Ask Question"):
                user_input(user_question, api_key)

    st.markdown("""""", unsafe_allow_html=True)    
    st.markdown("""""", unsafe_allow_html=True)    
    st.markdown("""""", unsafe_allow_html=True)    
    st.markdown("""
        <div style="text-align: center;">
            <a href="https://interactive.convai.com/character-id=e4c3a900-2092-11ef-9459-42010a7be00e">
                <img src="https://i.ibb.co/rMpvTyq/Galactice.png" class="glow-on-hover" height=250 width=1000>
            </a>
        </div>
    """, unsafe_allow_html=True)    

    ########### Career Snapshot ##############
    with st.container():
        st.markdown("""""")
        st.subheader('📌 Career Snapshot')
        components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Styles for the slideshow -->
        <style>
            body{{
                    font-family: sans-serif;
                }}
                .timeline{{                
                    position: relative;
                    max-width: 1200px;
                    margin: 100px auto;
                }}
                .container{{
                    padding: 10px 50px;
                    position: relative;
                    width: 40%;
                    animation: movedown 1s linear forwards;
		    
                }}
    
                @keyframes movedown{{
                    0%{{
                        opacity: 1;
                        transform: translateY(-30px);
                    }}
                    100%{{
                        opacity: 1;
                        transform: translateY(0px);
                    }}
                }}
                
                .text-box{{
                    padding: 20px 30px;
                    background: rgba(255, 255, 255, 0.2); 
		    color: rgba(255, 255, 255, 0.7);
                    position: relative;
                    border-radius: 6px;
                    font-size: 15px;
                }}
                
                .left-container{{
                    left:0;
                }}

                .right-container{{
                    left:50%;
                }}
                .container img{{
                    position: absolute;
                    width: 50px;
                    border-radius: 50%;
                    right: -45px;
                    top: 52px;
                    z-index: 10;
                    height: 50px;
                }}
                .right-container img{{
                    left:-25px;
                }}
                .timeline::after{{
                    content: '';
                    position: absolute;
                    width: 6px;
                    height: 100%;
		    background: rgba(255, 255, 255, 0.2); /* Adjust the transparency as needed */
                    top: 0;
                    left: 50%;
                    margin-left: -3px;
                    z-index: -1;
                    animation: moveline 6s linear forwards;
                }}
                
                @keyframes moveline{{
                    0%{{
                        height: 0;
                    }}
                    100%{{
                        height: 100%;
                    }}
                }}
                .text-box h2{{
                    font-weight: 600;
		    color: rgba(255, 255, 255, 0.8);
                }}
                .text-box small{{
                    display: inline-block;
                    margin: 15px;
		    color: rgba(255, 255, 255, 0.7);
                }}
                .left-container-arrow{{
                    height: 0;
                    width: 0;
                    position: absolute;
                    top: 50px;
                    z-index: 1;
                    border-top: 15px solid transparent;
                    border-bottom: 15px solid transparent;
                    border-left: 15px solid rgba(255, 255, 255, 0.4); ;
                    right: -14.5px;
                }}
                
                .right-container-arrow{{
                    height: 0;
                    width: 0;
                    position: absolute;
                    top: 50px;
                    z-index: 1;
                    border-top: 15px solid transparent;
                    border-bottom: 15px solid transparent;
                    border-right: 15px solid rgba(255, 255, 255, 0.4); ;
                    left: -15px;
                }}
                .container:nth-child(1){{
                    animation-delay: 0s;  
                }}
                .container:nth-child(2){{
                    animation-delay: 1s;
                }}
                .container:nth-child(3){{
                    animation-delay: 2s;
                }}
                .container:nth-child(4){{
                    animation-delay: 3s;   
                }}
            </style>
       
        </head>
        <body>
            <div class="timeline">
                <div class="container left-container">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRx2CV_ivX4ndCD9iJkSxJEZCy6-h23DdC9luNcGvXgw&s">
                    <div class="text-box">
                        <h2> University of Pune </h2>
                        <small> 2010-2014 </small>
                        <p> Pranav, a distinguished merit scholar, earned his engineering degree in Electronics and Telecommunication (E&TC) from Pune University.</p>
                        <span class="left-container-arrow"></span>
                    </div>
                </div>
        
                <div class="container right-container">
                    <img src="https://asset.brandfetch.io/id44tJQbVE/idv_dYAgEY.jpeg">
                    <div class="text-box">
                        <h2> Accenture Technology </h2>
                        <small> 2015-2017 </small>
                        <p> After completing his engineering degree, Pranav joined the software service giant Accenture, where he worked as a software developer specializing in SQL, Mainframe, and Java.</p>
                        <span class="right-container-arrow"></span>
        
                    </div>
                </div>
                <div class="container left-container">
                    <img src="https://iimbg.ac.in/wp-content/uploads/2020/01/IIMBG_LOGO_With_Space-01-1-300x214.jpg">
                    <div class="text-box">
                        <h2> Indian Institute of Management, Bodh Gaya </h2>
                        <small> 2017-2019 </small>
                        <p> After gaining around two years of industry experience, Pranav aced the CAT exam and was selected for the MBA program at IIM Bodh Gaya. He completed the two-year program with a gold medal 🥇</p>
                        <span class="left-container-arrow"></span>
        
                    </div>
                </div>
                <div class="container right-container">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwVCI1bU-FWO7jNoG3cHGkMtRSmoJDvsTqAIeqrRaplA&s">
                    <div class="text-box">
                        <h2> Business Consultant @ EY India </h2>
                        <small> 2019-2022 </small>
                        <p> Following his MBA, he secured a position as a business consultant with one of the prestigious Big 4 firms. At EY India, he spent approximately three years working on digital transformation and emerging technologysuch AI, data strategy, RPA, etc. initiatives</p>
                        <span class="right-container-arrow"></span>
                    </div>
                </div>
		<div class="container left-container">
                    <img src="https://asset.brandfetch.io/id44tJQbVE/idv_dYAgEY.jpeg">
                    <div class="text-box">
                        <h2> Management Consultant @ Accenture Strategy </h2>
                        <small> 2022-Present </small>
                        <p>After working nearly three years at EY, he transitioned to Accenture Strategy. There, he developed proof-of-concepts and was actively involved in various Generative AI projects. He contributed to a public service Generative AI strategy for multiple state and federal governments, assessed data maturity, and crafted a data and analytics strategy for public service agencies.</p>
                        <span class="left-container-arrow"></span>
        
                    </div>
                </div>
		
            </div>
        </body>
        </html> 
        """, height=1600)



    with st.container():
    # Divide the container into three columns
        col1,col2 = st.columns([0.475, 0.475])
        
    # In the first column (col1)        
    with col1:
        # Add a subheader to introduce the coworker endorsement slideshow
        st.subheader("🎖️ Coworker Endorsements")
        # Embed an HTML component to display the slideshow
        components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Styles for the slideshow -->
        <style>
            * {{box-sizing: border-box;}}
            .mySlides {{display: none;}}
            img {{vertical-align: middle;}}

            /* Slideshow container */
            .slideshow-container {{
            position: relative;
            margin: auto;
            width: 100%;
            }}

            /* The dots/bullets/indicators */
            .dot {{
            height: 15px;
            width: 15px;
            margin: 0 2px;
            background-color: #eaeaea;
            border-radius: 50%;
            display: inline-block;
            transition: background-color 0.6s ease;
            }}

            .active {{
            background-color: #6F6F6F;
            }}

            /* Fading animation */
            .fade {{
            animation-name: fade;
            animation-duration: 1s;
            }}

            @keyframes fade {{
            from {{opacity: .4}} 
            to {{opacity: 1}}
            }}

            /* On smaller screens, decrease text size */
            @media only screen and (max-width: 300px) {{
            .text {{font-size: 11px}}
            }}
            </style>
        </head>
        <body>
            <!-- Slideshow container -->
            <div class="slideshow-container">
                <div class="mySlides fade">
                <img src="https://i.ibb.co/Jmx4H6g/testimony-3.png" style="width:90%">
                </div>

                <div class="mySlides fade">
                <img src="https://i.ibb.co/hDYTd5n/testimony-1.png" style="width:90%">
                </div>

                <div class="mySlides fade">
                <img src="https://i.ibb.co/8mctPzk/testimony-2.png" style="width:90%">
                </div>

            </div>
            <br>
            <!-- Navigation dots -->
            <div style="text-align:center">
                <span class="dot"></span> 
                <span class="dot"></span> 
                <span class="dot"></span> 
            </div>

            <script>
            let slideIndex = 0;
            showSlides();

            function showSlides() {{
            let i;
            let slides = document.getElementsByClassName("mySlides");
            let dots = document.getElementsByClassName("dot");
            for (i = 0; i < slides.length; i++) {{
                slides[i].style.display = "none";  
            }}
            slideIndex++;
            if (slideIndex > slides.length) {{slideIndex = 1}}    
            for (i = 0; i < dots.length; i++) {{
                dots[i].className = dots[i].className.replace("active", "");
            }}
            slides[slideIndex-1].style.display = "block";  
            dots[slideIndex-1].className += " active";
            }}

            var interval = setInterval(showSlides, 2500); // Change image every 2.5 seconds

            function pauseSlides(event)
            {{
                clearInterval(interval); // Clear the interval we set earlier
            }}
            function resumeSlides(event)
            {{
                interval = setInterval(showSlides, 2500);
            }}
            // Set up event listeners for the mySlides
            var mySlides = document.getElementsByClassName("mySlides");
            for (i = 0; i < mySlides.length; i++) {{
            mySlides[i].onmouseover = pauseSlides;
            mySlides[i].onmouseout = resumeSlides;
            }}
            </script>

            </body>
            </html> 

            """,
                height=270,
    )  

# -----------------  contact  ----------------- #
    with col2:
        st.subheader("📨 Contact Me")
        contact_form = f"""
        <form action="https://formsubmit.co/baviskarpranav@gmail.com" method="POST">
            <input type="hidden" name="_captcha value="false"> <br/><br/>
            <input type="text" name="name" size="50" placeholder="   Your name" required> <br/><br/>
            <input type="email" name="email" size="50" placeholder="   Your email" required><br/><br/>
            <textarea name="message" rows="6" cols="50" placeholder="    Your message here" required></textarea> <br/><br/>
            <button type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)
        pdf_docs = ["pranav_baviskar_cv.pdf"]
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks, api_key)


if __name__ == "__main__":

    st.markdown('''<style>
        .stApp > header {
        background-color: transparent;
    }
    .stApp {
        background: linear-gradient(45deg, #3a5683 20%, #3a5683 45%, #0E1117 55%, #3a5683 90%);
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
