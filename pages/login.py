import streamlit as st
from utils import validator, hash
from services.auth_service import Login
from pages.header import render_header

render_header()

if "user" not in st.session_state:
    st.session_state.current_user = None


with st.form("Login"):
    username = st.text_input("Enter Your Username", placeholder="Username")
    password = st.text_input("Enter Your Password",placeholder="Password",type="password")
    Button = st.form_submit_button("Login")


if Button:
    # Validate Username
    if validator.validate_username(username):
        # Validate Password
        if validator.validate_password(password):
            print(type(password))
            secured_password = hash.secure_password(password)
            print(secured_password)

            obj = Login(username,secured_password)

            # Varify Login
            if obj.status == True:
                st.success("Log in successful")
                st.session_state.current_user = username
                st.switch_page("pages/home.py")

            elif obj.status == "user not found":
                st.error("User not found")

            else:
                st.error("Wrong Password")
        
        else:
            st.error("Password must be atleast 8 characters long")

    else:
        st.error("Username must be at least 4 characters")
