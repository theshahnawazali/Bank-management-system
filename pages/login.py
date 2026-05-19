import streamlit as st
from utils import validator, hash
from services.auth_service import Login
from pages.header import render_header
from utils.auth import login_user, load_user
from utils.auth import login_handle

st.set_page_config(page_title="Login", layout="wide")

current_user = load_user()

if current_user != None:
    st.switch_page("pages/home.py")


render_header(current_user)

st.markdown("### 👤 User Login")

with st.form("Login"):
    username = st.text_input("Enter Your Username", placeholder="Username")
    password = st.text_input("Enter Your Password",placeholder="Password",type="password")
    Button = st.form_submit_button("Login")


if Button:
    # Validate Username
    username = username.lower().strip()
    if validator.validate_username(username):
        # Validate Password
        if validator.validate_password(password):
            
            user = login_handle(username)


            if user == None:
                st.error("Incorrect Username")
                st.stop()

            else: 
                verify_password = hash.verify_password(password,user[0])

                if verify_password:
                    st.success("Login Successfull")
                    # st.switch_page("pages/home.py")
                    # login_user(username)
                else:
                    st.error("Incorrect Password")
        
        else:
            st.error("Password must be atleast 8 characters long")

    else:
        st.error("Username must be at least 4 characters")
