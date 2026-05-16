import streamlit as st
from utils import validator
from services.bank_service import get_account
from pages.header import render_header

render_header(st.session_state.current_user)

if validator.validate_user_logged_in(st.session_state.current_user):
    user = get_account(st.session_state.current_user)
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