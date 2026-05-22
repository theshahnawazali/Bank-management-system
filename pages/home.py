import streamlit as st
from utils import validator
from services.bank_service import get_account
from pages.header import render_header
from utils.verify_login import verify_login_session
from utils.auth import load_user


st.set_page_config(
    page_title="Home Page",
    layout="wide"
)

user = verify_login_session()

if user == None:
    st.switch_page("app.py")

# ---------------- HEADER ----------------
render_header(user["username"])

st.title(f"Hello {user["name"]}")

st.markdown("### Our Services ")

col1, col2, col3, col4, col5 = st.columns([2,2,2,2,2])


st.markdown("""
    <style>
    [data-testid="column"] .stButton > button {
        height: 150px;
    }
    </style>
""", unsafe_allow_html=True)

# # ---------------- ACCOUNT INFO ----------------
with col1:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("🏦 Account\nInfo", use_container_width=True):
        st.switch_page("pages/info.py")

# ---------------- DEPOSIT ----------------
with col2:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("💰 Deposit", use_container_width=True):
        st.switch_page("pages/deposit.py")

# ---------------- WITHDRAW ----------------
with col3:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("💸 Withdraw", use_container_width=True):
        st.switch_page("pages/withdraw.py")

# ---------------- TRANSFER ----------------
with col4:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("🔄 Transfer", use_container_width=True):
        st.switch_page("pages/transfer.py")

# ---------------- TRANSACTIONS ----------------
with col5:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("📊 Transactions", use_container_width=True):
        st.switch_page("pages/transaction.py")
