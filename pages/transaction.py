import streamlit as st
from templates import header,sidebar
from services.bank_service import Transactions
from utils.verify_login import verify_login_session


st.set_page_config(page_title="📊 Transactions",layout="wide")

# --------------------- Headers -----------------------------
sidebar.sidebar()
header.user_header("Transaction")

# ----------------- Verify Login ----------------------------
user = verify_login_session()

if user == None:
    st.switch_page("app.py")


st.markdown("### 📊 All Transactions")

st.write("Will implemented soon")