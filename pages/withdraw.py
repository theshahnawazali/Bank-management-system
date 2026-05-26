import streamlit as st
from services.bank_service import Withdraw
from pages.header import render_header
from utils.verify_login import verify_login_session
from templates import sidebar,header

st.set_page_config(
    page_title="Withdraw",
    layout="wide"
)

user = verify_login_session()

if user == None:
    st.switch_page("app.py")

# ---------------- HEADER ----------------

sidebar.sidebar()
header.user_header("Withdraw",user["name"])


with st.form("Withdrawal-form"):
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
            <span class='big-text'>Withdraw Funds</span>
            <span class='small-text'>Enter the amount you wants to withdraw from your account</span>
        </div>
    """,unsafe_allow_html=True)

    amount = st.text_input("Enter Amount:",placeholder="Amount")
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

        except ValueError:
            st.error("Enter Number Only")