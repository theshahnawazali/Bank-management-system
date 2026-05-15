import streamlit as st
from utils import validator
from services.bank_service import Deposit, Withdraw, Transactions, Transfer, get_account
from pages.header import render_header

 # ---------------- HEADER ----------------
render_header(st.session_state.current_user)


if st.button("LogOut"):
    st.switch_page("./app.py")
    st.session_state.current_user = None

 # ---------------- ACCOUNT INFO ----------------
if st.button("Account Info"):
    if validator.validate_user_logged_in(st.session_state.current_user):
        user = get_account(st.session_state.current_user)
        for key, value in user.info.items():
            st.write(f"{key} : {value}")
    
    else:
        st.error("User Must Be login first")

 # ---------------- DEPOSIT ----------------
if st.button("Deposit"):
    if validator.validate_user_logged_in(st.session_state.current_user):
        st.switch_page("pages/deposit.py")

 # ---------------- WITHDRAW ----------------
if st.button("Withdraw"):
    if validator.validate_user_logged_in(st.session_state.current_user):
        st.switch_page("pages/withdraw.py")

 # ---------------- TRANSFER ----------------
if st.button("Transfer"):
    if validator.validate_user_logged_in(st.session_state.current_user):
        st.switch_page("pages/transfer.py")

 # ---------------- TRANSACTIONS ----------------
if st.button("Transactions"):
    if validator.validate_user_logged_in(st.session_state.current_user):
        pass