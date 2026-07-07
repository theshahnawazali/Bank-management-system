import streamlit as st
from core import security
from utils import validator
from backend.pages.header import render_header
from utils.auth import load_user,login_handle
from utils.login import update_login_info
from utils.verify_login import verify_login_session

st.set_page_config(page_title="Login", layout="wide")

current_user = load_user()

user = verify_login_session()

if user == None:
    pass
else:
    st.switch_page("pages/home.py")

render_header(current_user)

st.markdown("### 👤 User Login")

with st.form("Login"):
    username = st.text_input(
        "Enter Your Username",
        placeholder="Username"
        )
    
    password = st.text_input(
        "Enter Your Password",
        placeholder="Password",
        type="password"
        )
    
    button = st.form_submit_button("Login")


if button:

    # Validate Username
    username = username.lower().strip()

    if validator.validate_username(username):
        
        if validator.validate_password(password):
            
            user = login_handle(username)


            if user == None:
                st.error("Incorrect Username")
                st.stop()

            else: 
                verify_password = security.verify_password(
                    password,
                    user[0]
                    )

                if verify_password:
                    st.success("Login Successfull")
                    
                    # Upadate login info
                    update_login_info(username)
                    
                    st.switch_page("pages/home.py")

                else:
                    st.error("Incorrect Password")
        
        else:
            st.error("Password must be atleast 8 characters long")

    else:
        st.error("Username must be at least 4 characters")
