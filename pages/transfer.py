import streamlit as st
from services.bank_service import Transfer
from pages.header import render_header
from utils.auth import load_user
from utils.verify_login import verify_login_session

st.set_page_config(
    page_title="Transfer",
    layout="wide"
)

user = verify_login_session()

if user == None:
    st.switch_page("app.py")

# ---------------- HEADER ----------------
render_header(user["username"])


st.markdown("### Amount Transfer Form")

with st.form("Transfer"):
    Account_number = st.text_input("Enter Account Number",placeholder="Account Number")
    Amount = st.text_input("Enter Amount",placeholder="Amount")
    btn = st.form_submit_button("Transfer")

if btn:
    try:
        Amount = float(Amount)

        if Amount <= 0:
            st.error("Amount should be greater then 0")
            st.stop()

        status = Transfer(user["username"],Amount,Account_number)
        

        if status.transfer:
            st.success("Amount Transfer Successfull")
            st.switch_page("pages/home.py")
        else:
            st.error("Insufficient Amount")
    
    except ValueError:
        st.error("Amount should be in Number Only")