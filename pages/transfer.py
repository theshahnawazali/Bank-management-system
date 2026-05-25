import streamlit as st
from services.bank_service import Transfer
from templates import header
from utils.verify_login import verify_login_session
from templates import sidebar

st.set_page_config(
    page_title="Transfer",
    layout="wide"
)

user = verify_login_session()

if user == None:
    st.switch_page("app.py")

# ---------------- HEADER ----------------
header.user_header("Transfer")
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
            <span class='big-text'>Transfer Funds</span>
            <span class='small-text'>Tranfer your money safe and securely</span>
        </div>
    """,unsafe_allow_html=True)
    account_number = st.text_input("Enter Account Number",placeholder="Account Number")
    amount = st.text_input("Enter Amount:",placeholder="Amount")
    btn = st.form_submit_button("Transfer")

    if btn:
        try:
            if account_number == "" or amount == "":
                st.error("Enter Account Number and Amount")
                st.stop()

            amount = float(amount)

            if len(account_number) != 12:
                st.error("Enter Valid Account Number")
                st.stop()

            if amount <= 0:
                st.error("Enter Amount Greater then 0")
                st.stop()

            status = Transfer(user["username"],amount,account_number)
        

            if status.transfer:
                st.success("Amount Transfer Successfull")
                st.switch_page("pages/home.py")
            else:
                st.error("Insufficient Amount")
            

        except ValueError:
            st.error("Enter Number Only")