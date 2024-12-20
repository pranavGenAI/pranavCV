import streamlit as st
# Add custom CSS for styling the app
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #6c83e1, #4bc4d4);
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }
    .title {
        color: #ffffff;
        font-size: 36px;
        text-align: center;
        font-weight: bold;
        margin-top: 30px;
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
    .logo {
        display: block;
        margin: 20px auto;
        max-width: 150px;
        transition: all 0.3s ease;
    }
    .logo:hover {
        transform: rotate(10deg);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
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

# Display the NHS logo at the top with a reduced size and subtle hover effect
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/National_Health_Service_%28England%29_logo.svg/2560px-National_Health_Service_%28England%29_logo.svg.png", 
         width=150, use_column_width=False)


# Capture UID input from the user in a beautiful input box
with st.form(key='uid_form'):
    st.markdown('<div class="input-container"><label class="input-label">Please enter your UID:</label></div>', unsafe_allow_html=True)
    uid = st.text_input("", label_visibility="hidden", placeholder="Enter your UID here", help="Enter your unique identifier", max_chars=50)
    submit_button = st.form_submit_button(label="Submit", use_container_width=True)
    
# Handle form submission and redirection
if submit_button:
    if uid:
        st.success(f"UID {uid} captured successfully!")
        # JavaScript for redirection
        st.markdown(
            """
            <script type="text/javascript">
            window.location.href = "https://www.google.com";
            </script>
            """, unsafe_allow_html=True
        )
    else:
        st.error("Please enter a valid UID.")
