import streamlit as st
from utils import validator
from services.bank_service import get_account
from templates import header
from utils.verify_login import verify_login_session
from templates import sidebar,overview
from services.bank_service import get_account


st.set_page_config(
    page_title="Home Page",
    layout="wide",
    initial_sidebar_state="expanded"
)
user = verify_login_session()

if user == None:
    st.switch_page("app.py")


# ---------------- HEADER ----------------
header.user_header("")

current_user = get_account(user["username"]).info

data = {
    "name" : current_user["Name"],
    "Balance" : current_user["Balance"],
    "Account Number" : current_user["Account Number "],
    "Account Username" : current_user["Account Username"],
    "Account Type" : current_user["Account Type"],
    "Open On"      : current_user["Open On"]
}

overview.user_overview(data)
sidebar.sidebar()


st.markdown("""
    <style>
    .service-box {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 14px;
        width : 100%;
        margin : 2px;
        height : 180px;
        padding : 15px;
        display : flex;
        flex-direction:column;
        gap:5px;
        }
    .icons {
        font-size : 30px;
    }
    .service-name {
        font-size:18px;
        font-weight:bold;
        line-height:35px;
        text-align : left;
    }
    .msg {
        font-size : 15px;
        color: gray;
    }
    </style>
    """,unsafe_allow_html=True)

col_withdraw, col_deposit, col_transfer, col_transaction = st.columns([2,2,2,2])

with col_withdraw:
    st.markdown("""<div class="service-box">
                    <span class='icons'>💸</span> 
                    <span class='service-name'>Withdraw</span> 
                    <span class='msg' >Withdraw your funds easily and quickly</span>
                """,unsafe_allow_html=True)

with col_deposit:
    st.markdown("""<div class="service-box">
                <span class='icons'>💰</span> 
                <span class='service-name'>Deposit</span> 
                <span class='msg' >Add funds to your account securely</span>
                </div>""",unsafe_allow_html=True)

with col_transfer:
    st.markdown("""<div class="service-box">
                    <span class='icons'>🔄</span>
                    <span class='service-name'>Transfer</span>
                    <span class='msg'>Send money to other accounts instantly</span>
                </div>""",unsafe_allow_html=True)

with col_transaction:
    st.markdown("""
                <div class="service-box">
                    <span class='icons'>📊</span>
                    <span class='service-name'>Transaction</span>
                    <span class='msg'>View your recent Trasactions</span>
                </div>
                """,unsafe_allow_html=True)