# header.py
import streamlit as st


current_user_username = "User"


if st.button("Login"):
    st.switch_page("pages/login.py")

if st.button("Signup"):
    st.switch_page("pages/signup.py")