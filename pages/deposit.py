import streamlit as st
from services.bank_service import Deposit


with st.form("Deposit"):
    amount = st.text_input("Enter Amount",placeholder="Amount")
    btn = st.form_submit_button("Deposit")

if btn:
    
    print(st.session_state.current_user)
    if amount.isdigit():
        amount = int(amount)
        Deposit(st.session_state.current_user, amount)
        st.switch_page("pages/home.py")
        
    else:
        st.error("Enter Number Only")