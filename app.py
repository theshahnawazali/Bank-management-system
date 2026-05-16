# header.py
import streamlit as st
from pages.header import render_header



if "user" not in st.session_state:
    st.session_state.current_user = None

render_header(st.session_state.current_user)

# if st.button("Login",key="main_login"):
#     st.switch_page("pages/login.py")

# if st.button("Signup",key="main_signup"):
#     st.switch_page("pages/signup.py")