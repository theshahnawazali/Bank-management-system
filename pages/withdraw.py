import streamlit as st
from services.bank_service import Withdraw
from pages.header import render_header
from utils.auth import load_user

current_user = load_user()

render_header(current_user)


with st.form("Deposit"):
    amount = st.text_input("Enter Amount",placeholder="Amount")
    btn = st.form_submit_button("Deposit")

if btn:
    
    print(st.session_state.current_user)
    if amount.isdigit():
        amount = int(amount)
        Withdraw(st.session_state.current_user, amount)
        st.switch_page("pages/home.py")
        
    else:
        st.error("Enter Number Only")