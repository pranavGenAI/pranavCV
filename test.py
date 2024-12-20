import streamlit as st
import webbrowser

# Display the NHS logo at the top
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/National_Health_Service_%28England%29_logo.svg/2560px-National_Health_Service_%28England%29_logo.svg.png", width=200)


# Capture UID input from the user
uid = st.text_input("Please enter your UID:")

# Button to submit UID
if st.button("Submit"):
    if uid:
        # Show a success message and redirect
        st.success(f"UID {uid} captured successfully!")
        # Redirect user to Google after a short delay
        webbrowser.open("https://www.google.com")
    else:
        st.error("Please enter a valid UID.")
