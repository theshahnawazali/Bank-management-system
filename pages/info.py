import streamlit as st
from utils import validator
from services.bank_service import get_account
from pages.header import render_header
from utils.auth import load_user

current_user = load_user()

render_header(current_user)

st.markdown("### User Informations")

if validator.validate_user_logged_in(current_user):
    user = get_account(current_user)
    for key, value in user.info.items():
        st.write(f"{key} : {value}")

else:
    st.error("User Must Be login first")


st.markdown("## Quick Access")

col1, col2 = st.columns([1,1])

with col1:
    if st.button("Home",key="quick_home_page"):
        st.switch_page("pages/home.py")

with col2:
    if st.button("Transaction",key="quick_transaction_page"):
        # st.switch_page("")
        pass