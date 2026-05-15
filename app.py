# header.py
import streamlit as st
from pages.header import render_header

render_header()

if "user" not in st.session_state:
    st.session_state.current_user = None


if st.button("Login"):
    st.switch_page("pages/login.py")

if st.button("Signup"):
    st.switch_page("pages/signup.py")