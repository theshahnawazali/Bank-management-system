import streamlit as st
from utils import validator
from services.bank_service import get_account
from pages.header import render_header
from utils.auth import load_user

current_user = load_user()




if current_user is None:
    st.switch_page("app.py")


# ---------------- HEADER ----------------
render_header(current_user)

st.title(f"Hello {current_user}")

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
        if validator.validate_user_logged_in(current_user):
            st.switch_page("pages/deposit.py")

# ---------------- WITHDRAW ----------------
with col3:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("💸 Withdraw", use_container_width=True):
        if validator.validate_user_logged_in(current_user):
            st.switch_page("pages/withdraw.py")

# ---------------- TRANSFER ----------------
with col4:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("🔄 Transfer", use_container_width=True):
        if validator.validate_user_logged_in(current_user):
            st.switch_page("pages/transfer.py")

# ---------------- TRANSACTIONS ----------------
with col5:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("📊 Transactions", use_container_width=True):
        if validator.validate_user_logged_in(current_user):
            st.switch_page("pages/transaction.py")
