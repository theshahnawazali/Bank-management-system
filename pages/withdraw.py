import streamlit as st
from services.bank_service import Withdraw
from pages.header import render_header
from utils.verify_login import verify_login_session

st.set_page_config(
    page_title="Withdraw",
    layout="wide"
)

user = verify_login_session()

if user == None:
    st.switch_page("app.py")

# ---------------- HEADER ----------------
render_header(user["username"])

st.markdown("### Amount Withdrawal Form")

with st.form("Deposit"):
    amount = st.text_input("Enter Amount",placeholder="Amount")
    btn = st.form_submit_button("Withdraw")

if btn:
    try:
        amount = float(amount)

        if amount <= 0:
            st.error("Enter Amount Greater then 0")


        status = Withdraw(user["username"],amount)

        if status.withdraw:
            st.success("Withdrawal Successfull")
            st.switch_page("pages/home.py")

        else:
            st.error("Insufficient Withdrawal Amount")

    except ValueError:
        st.error("Enter Number Only")