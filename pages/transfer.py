import streamlit as st
from services.bank_service import Transfer
from pages.header import render_header

render_header(st.session_state.current_user)

with st.form("Transfer"):
    Account_number = st.text_input("Enter Account Number",placeholder="Account Number")
    Amount = st.text_input("Enter Amount",placeholder="Amount")
    btn = st.form_submit_button("Transfer")

if btn:
    if Amount.isdigit():
        Amount = int(Amount)
        Transfer(st.session_state.current_user,Amount,Account_number)
        st.success("Amount Transfer Successful")
        st.switch_page("pages/home.py")
