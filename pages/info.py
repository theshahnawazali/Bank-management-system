import streamlit as st
from utils import validator
from services.bank_service import get_account
from pages.header import render_header
from utils.auth import load_user
from utils.verify_login import verify_login_session

st.set_page_config(
    page_title="Account Info",
    layout="wide"
)

user = verify_login_session()

if user == None:
    st.switch_page("app.py")

# ---------------- HEADER ----------------
render_header(user["username"])

st.markdown("### User Informations")

# if validator.validate_user_logged_in(user["username"]):
#     user = get_account(user["username"])
#     for key, value in user.info.items():
#         st.write(f"{key} : {value}")

# else:
#     st.error("User Must Be login first")

user = get_account(user["username"])
for key, value in user.info.items():
    st.write(f"{key} : {value}")


st.markdown("## Quick Access")

col1, col2 = st.columns([1,1])

with col1:
    if st.button("Home",key="quick_home_page"):
        st.switch_page("pages/home.py")

with col2:
    if st.button("Transaction",key="quick_transaction_page"):
        # st.switch_page("")
        pass