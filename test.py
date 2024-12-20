import streamlit as st
import webbrowser

# Add custom CSS for styling the app
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .title {
        color: #1e3a8a;
        font-size: 36px;
        text-align: center;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .button:hover {
        background-color: #45a049;
    }
    .logo {
        display: block;
        margin: 0 auto;
        max-width: 200px;
    }
    .input-container {
        text-align: center;
    }
    .input-label {
        font-size: 18px;
        color: #333;
        margin-bottom: 10px;
    }
    .input-field {
        font-size: 18px;
        padding: 10px;
        width: 70%;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .message {
        font-size: 16px;
        text-align: center;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display the NHS logo at the top
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/National_Health_Service_%28England%29_logo.svg/2560px-National_Health_Service_%28England%29_logo.svg.png", width=200, use_column_width=True)

# Title for the app with modern font and color
st.markdown('<h1 class="title">UID Capture and Redirect</h1>', unsafe_allow_html=True)

# Capture UID input from the user in a beautiful input box
with st.form(key='uid_form'):
    st.markdown('<div class="input-container"><label class="input-label">Please enter your UID:</label></div>', unsafe_allow_html=True)
    uid = st.text_input("", key="uid_input", label_visibility="hidden", placeholder="Enter UID here", help="Enter your unique identifier", max_chars=50, key="uid_input")
    submit_button = st.form_submit_button(label="Submit", use_container_width=True, disabled=False)
    
# Handle form submission and redirection
if submit_button:
    if uid:
        st.success(f"UID {uid} captured successfully!")
        # Redirect user to Google after a short delay
        webbrowser.open("https://www.google.com")
    else:
        st.error("Please enter a valid UID.")

