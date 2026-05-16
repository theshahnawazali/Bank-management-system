import streamlit as st
from utils import validator
from services.bank_service import get_account
from pages.header import render_header
from utils.auth import load_user

current_user = load_user()




if st.session_state.current_user == None:
    st.switch_page("app.py")


 # ---------------- HEADER ----------------
render_header(current_user)

# st.markdown("### Services ")

col1, col2, col3 = st.columns([2,2,2])
col4, col5 = st.columns([2,2])


st.markdown("""
    <style>
    div.stButton > button[kind="primary"],type="primary" {
        width : 200px;
        height : 150px;
        font-size : 50px;
        backgrond-color : #131720
        }
    .login-btn button {
            
        }
    </style>
    """,unsafe_allow_html=True)

# ---------------- ACCOUNT INFO ----------------
with col1:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("Account Info",type="primary"):
        st.switch_page("pages/info.py")

# ---------------- DEPOSIT ----------------
with col2:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("Deposit",type="primary"):
        if validator.validate_user_logged_in(st.session_state.current_user):
            st.switch_page("pages/deposit.py")

# ---------------- WITHDRAW ----------------
with col3:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("Withdraw",type="primary"):
        if validator.validate_user_logged_in(st.session_state.current_user):
            st.switch_page("pages/withdraw.py")

# ---------------- TRANSFER ----------------
with col4:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("Transfer",type="primary"):
        if validator.validate_user_logged_in(st.session_state.current_user):
            st.switch_page("pages/transfer.py")

# ---------------- TRANSACTIONS ----------------
with col5:
    st.markdown("<div class='boxes'>",unsafe_allow_html=True)

    if st.button("Transactions",type="primary"):
        if validator.validate_user_logged_in(st.session_state.current_user):
            pass



# import streamlit as st
# from utils import validator
# from services.bank_service import get_account
# from pages.header import render_header

# if st.session_state.current_user == None:
#     st.switch_page("app.py")

# render_header(st.session_state.current_user)

# col1, col2, col3 = st.columns([2,2,2])
# col4, col5 = st.columns([2,2])

# # CSS
# st.markdown("""
# <style>
# div.stButton > button {
#     width: 200px;
#     height: 100px;
#     font-size: 24px;
# }
# </style>
# """, unsafe_allow_html=True)

# with col1:
#     if st.button("Account Info"):
#         st.switch_page("pages/info.py")

# with col2:
#     if st.button("Deposit"):
#         if validator.validate_user_logged_in(st.session_state.current_user):
#             st.switch_page("pages/deposit.py")

# with col3:
#     if st.button("Withdraw"):
#         if validator.validate_user_logged_in(st.session_state.current_user):
#             st.switch_page("pages/withdraw.py")

# with col4:
#     if st.button("Transfer"):
#         if validator.validate_user_logged_in(st.session_state.current_user):
#             st.switch_page("pages/transfer.py")

# with col5:
#     if st.button("Transactions"):
#         pass