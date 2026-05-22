import streamlit as st
st.set_page_config(
    page_title="Withdraw",
    layout="wide"
)


from services.bank_service import Deposit
from pages.header import render_header
from utils.auth import load_user
from utils.verify_login import verify_login_session


user = verify_login_session()


if not user:
    st.error("Please login again")
    st.stop()


if user == None:
    st.switch_page("app.py")

# ---------------- HEADER ----------------
render_header(user["username"])

st.markdown("### Amount Deposit Form")

with st.form("Deposit"):
    amount = st.text_input("Enter Amount",placeholder="Amount")
    btn = st.form_submit_button("Deposit")

if btn:
    try:
        amount = float(amount)

        if amount <= 0:
            st.error("Amount should be greater then 0")
            st.stop()

        status = Deposit(user["username"],amount)

        if status.deposit:
            st.success("Deposit Successfull")
            st.switch_page("pages/home.py")
        else:
            st.error("Insufficient Amount")

    except ValueError:
        st.error("Enter Number Only")