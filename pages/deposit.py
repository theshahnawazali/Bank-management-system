import streamlit as st

st.set_page_config(
    page_title="Deposit",
    layout="wide"
)

from templates import sidebar
from services.bank_service import Deposit
from templates import header
from utils.verify_login import verify_login_session

# -------------------- Verify Login -------------------
user = verify_login_session()

if user == None:
    st.switch_page("app.py")

# # ---------------- HEADER ----------------
header.user_header("Deposit")
sidebar.sidebar()

with st.form("Deposit-form"):
    st.markdown("""
        <style>
        .box {
            display : flex;
            flex-direction : column;
            height : auto;
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 14px;
            padding: 1.5rem;
            box-sizing: border-box;
            margin : 10px;
        }
        .main {
            display: flex;
            flex-direction: column;
        }
        .big-text  {
            font-size: 1.35rem;
            font-weight: 600;
            color: #e6edf3;
            margin-bottom: 3px;
            letter-spacing: 0.05em;
        }
        .small-text {
            font-size : 15px;
            color : grey; 
        }
        .custom-btn div.stButton > button {
            
        }
        </style>
        <div class='box'>
            <span class='big-text'>Deposit Funds</span>
            <span class='small-text'>Add funds to your selected account</span>
        </div>
    """,unsafe_allow_html=True)

    amount = st.text_input("Enter Amount:",placeholder="Amount")
    btn = st.form_submit_button("Deposit")

    if btn:
        try:
            amount = float(amount)
            if amount <= 0:
                st.error("Enter Amount Greater then 0")

            status = Deposit(user["username"],amount)

            if status.deposit:
                st.success("Withdrawal Successfull")
                st.switch_page("pages/home.py")

        except ValueError:
            st.error("Enter Number Only")