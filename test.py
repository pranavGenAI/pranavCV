import streamlit as st
import webbrowser

# Add custom CSS for styling the app with a new background and logo in the corner
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6); /* Blue gradient background */
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        position: relative;
    }
    .logo {
        position: absolute;
        top: 10px;
        left: 10px;
        width: 100px;
        transition: all 0.3s ease;
    }
    .logo:hover {
        transform: rotate(10deg);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .title {
        color: #ffffff;
        font-size: 36px;
        text-align: center;
        font-weight: bold;
        margin-top: 100px;
        text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    }
    .button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 28px;
        font-size: 20px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .button:hover {
        background-color: #45a049;
        box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.3);
        transform: translateY(-4px);
    }
    .input-container {
        text-align: center;
        margin-top: 20px;
    }
    .input-label {
        font-size: 18px;
        color: #ffffff;
        margin-bottom: 10px;
    }
    .input-field {
        font-size: 18px;
        padding: 12px;
        width: 80%;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }
    .message {
        font-size: 16px;
        text-align: center;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display the NHS logo at the top left corner, smaller size
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/National_Health_Service_%28England%29_logo.svg/2560px-National_Health_Service_%28England%29_logo.svg.png", 
         width=100, use_column_width=False)

# Title for the app with modern font and color
st.markdown('<h1 class="title">UID Capture and Redirect</h1>', unsafe_allow_html=True)

# Capture UID input from the user in a beautiful input box
with st.form(key='uid_form'):
    st.markdown('<div class="input-container"><label class="input-label">Please enter your UID:</label></div>', unsafe_allow_html=True)
    uid = st.text_input("", label_visibility="hidden", placeholder="Enter your UID here", help="Enter your unique identifier", max_chars=50)
    submit_button = st.form_submit_button(label="Submit", use_container_width=True)
    
# Handle form submission and redirection
if submit_button:
    if uid:
        st.success(f"UID {uid} captured successfully!")
        # Redirect user to Google after a short delay
        webbrowser.open("https://www.google.com")
    else:
        st.error("Please enter a valid UID.")
